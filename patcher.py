import requests
import re
import idna
from progress.bar import Bar
from python_hosts import Hosts, HostsEntry

LOBBIES_ENDPOINT = "https://api.sc2arcade.com/lobbies/active"
MAP_INFO_ENDPOINT = "https://api.sc2arcade.com/maps/{}/{}"
IMG_PATTERN = r'<img path="//[^"]+"/>'
DOMAIN_PATTERN = r"//(.+?)/"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"


def get_data(endpoint, params=None):
    response = requests.get(endpoint, params=params)
    try:
        return response.json()
    except:
        return None


def get_lobbies(regionId):
    return get_data(
        LOBBIES_ENDPOINT,
        {
            "regionId": regionId,
            "includeSlots": "false",
            "includeSlotsProfile": "false",
            "includeSlotsJoinInfo": "false",
            "includeJoinHistory": "false",
        },
    )


def get_map(regionId, mapId):
    return get_data(
        MAP_INFO_ENDPOINT.format(regionId, mapId),
        {
            "mapId": mapId,
        },
    )


def has_img_tag(text):
    return "<img" in text


def get_domains(text):
    matches = re.findall(IMG_PATTERN, text)
    domains = set()
    for match in matches:
        result = re.search(DOMAIN_PATTERN, match).group(1)
        domains.add(result)
    return domains


def punycode(domain):
    SPECIAL_DOMAINS = ["_", "-"]
    if domain in SPECIAL_DOMAINS:
        return domain
    return idna.encode(domain, uts46=True, std3_rules=True, transitional=True).decode()


def main():
    regionId = 1  # 1=America, 2=Europe, 3=Asia
    hasHostsPermission = False

    # check if there is write permission to the hosts file
    try:
        with open(HOSTS_PATH, "a+") as f:
            f.close()
            hasHostsPermission = True
    except PermissionError:
        print(
            "You don't have permission to write to the hosts file. You will only see the domains found in active lobbies."
        )

    # get lobbies
    print("Fetching lobbies...")
    lobbies = get_lobbies(regionId)

    # api is not working
    if type(lobbies) is not list:
        print("An error has occurred while fetching the lobbies.")
        return

    # filter those maps with only 1 human slot
    lobbies = [lobby for lobby in lobbies if lobby["slotsHumansTotal"] == 1]

    # get map and mod id
    mapIds = set()
    for lobby in lobbies:
        mapIds.add(lobby["mapBnetId"])
        mapIds.add(lobby["extModBnetId"])
    # convert to list
    mapIds = list(mapIds)

    # fetch the map info and extracts the domains in img tags
    # we simply read the info in English
    print("Fetching map info...")
    bar = Bar("Processing", max=len(mapIds))
    domains = set()
    for mapId in mapIds:
        map_info = get_map(regionId, mapId)
        if map_info is None:
            continue
        if "name" in map_info and has_img_tag(map_info["name"]):
            domains.update(get_domains(map_info["name"]))
        if "description" in map_info and has_img_tag(map_info["description"]):
            domains.update(get_domains(map_info["description"]))
        bar.next()
    bar.finish()

    # covert to punycode
    domains = [punycode(domain) for domain in domains]

    # prompt the user whether to write to hosts file
    print("These domains are found in active lobbies:")
    print(domains)
    print()

    if not hasHostsPermission:
        print("You don't have permission to write to the hosts file.")
        print("Exporting domains...")
        with open("domains.txt", "w") as f:
            for domain in domains:
                f.write(f"0.0.0.0 {domain}\n")
        print("Done. The domains are written to domains.txt. Add them to the hosts file manually.")
        print("If you want this program to write to the hosts file, run it as administrator.")
        input()
        return
    
    print("Do you want to write these domains to the hosts file? (y/n)")
    answer = input()
    if answer.lower() != "y":
        return

    # write to hosts file
    print("Writing to hosts file...")
    count_new = 0
    hosts = Hosts()
    for domain in domains:
        if hosts.exists(names=[domain]):
            continue

        entry = HostsEntry(entry_type="ipv4", address="0.0.0.0", names=[domain])
        hosts.add([entry])
        count_new += 1
    hosts.write()
    print(f"Done. Added {count_new} new entries.")
    input()


if __name__ == "__main__":
    main()
