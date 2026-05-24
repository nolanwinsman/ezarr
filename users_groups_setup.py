import os
import subprocess


# -----------------------------
# Helpers (safe idempotent checks)
# -----------------------------
def user_exists(username):
    return subprocess.run(
        ["id", username],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0


def group_exists(groupname):
    return subprocess.run(
        ["getent", "group", groupname],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0


def ensure_user(username, uid):
    if user_exists(username):
        print(f"[SKIP] user '{username}' already exists")
        return

    print(f"[CREATE] user '{username}' (uid {uid})")
    os.system(f"sudo useradd {username} -u {uid}")


def ensure_group(groupname, gid):
    if group_exists(groupname):
        print(f"[SKIP] group '{groupname}' already exists")
        return

    print(f"[CREATE] group '{groupname}' (gid {gid})")
    os.system(f"sudo groupadd -g {gid} {groupname}")


# -----------------------------
# Main class
# -----------------------------
class UserGroupSetup:
    def __init__(self, root_dir_ssd='/', root_dir_hdd='/'):
        self.root_dir_ssd = root_dir_ssd
        self.root_dir_hdd = root_dir_hdd

        ensure_group("mediacenter", 13000)

        os.system("sudo usermod -a -G mediacenter $USER")

        os.system(
            f"sudo mkdir -pv -m 775 "
            f"{self.root_dir_hdd}/data/{{media,usenet,torrents}} "
            f"{self.root_dir_hdd}/data/usenet/{{incomplete,complete}} "
            f"{self.root_dir_hdd}/data/torrents/{{incomplete,complete}} "
            f"&& sudo chown -R $(id -u):mediacenter {self.root_dir_hdd}/data"
        )

    def create_config_dir(self, service_name):
        os.system(
            f"sudo mkdir -p {self.root_dir_ssd}/config/{service_name}-config -m 775"
            f" && sudo chown -R {service_name}:mediacenter {self.root_dir_ssd}/config/{service_name}-config"
            f" && sudo chown $(id -u):mediacenter {self.root_dir_ssd}/config"
        )

    # -----------------------------
    # Servarr
    # -----------------------------
    def sonarr(self):
        ensure_user("sonarr", 13001)

        os.system(
            f"sudo mkdir -pv {self.root_dir_hdd}/data/{{media,usenet,torrents}}/{{anime,cartoons,tv}} -m 775"
            f" && sudo chown -R sonarr:mediacenter {self.root_dir_hdd}/data/{{media,usenet,torrents}}/{{anime,cartoons,tv}}"
        )

        self.create_config_dir("sonarr")
        os.system("sudo usermod -a -G mediacenter sonarr")

    def radarr(self):
        ensure_user("radarr", 13002)

        os.system(
            f"sudo mkdir -pv {self.root_dir_hdd}/data/{{media,usenet,torrents}}/{{anime_movies,cartoon_movies,documentaries,movies}} -m 775"
            f" && sudo chown -R radarr:mediacenter {self.root_dir_hdd}/data/{{media,usenet,torrents}}/{{anime_movies,cartoon_movies,documentaries,movies}}"
        )

        self.create_config_dir("radarr")
        os.system("sudo usermod -a -G mediacenter radarr")

    def lidarr(self):
        ensure_user("lidarr", 13003)

        os.system(
            f"sudo mkdir -pv {self.root_dir_hdd}/data/{{media,usenet,torrents}}/music -m 775"
            f" && sudo chown -R lidarr:mediacenter {self.root_dir_hdd}/data/{{media,usenet,torrents}}/music"
        )

        self.create_config_dir("lidarr")
        os.system("sudo usermod -a -G mediacenter lidarr")

    def readarr(self):
        ensure_user("readarr", 13004)

        os.system(
            f"sudo mkdir -pv {self.root_dir_hdd}/data/{{media,usenet,torrents}}/books -m 775"
            f" && sudo chown -R readarr:mediacenter {self.root_dir_hdd}/data/{{media,usenet,torrents}}/books"
        )

        self.create_config_dir("readarr")
        os.system("sudo usermod -a -G mediacenter readarr")

    def mylar3(self):
        ensure_user("mylar", 13005)

        os.system(
            f"sudo mkdir -pv {self.root_dir_hdd}/data/{{media,usenet,torrents}}/comics -m 775"
            f" && sudo chown -R mylar:mediacenter {self.root_dir_hdd}/data/{{media,usenet,torrents}}/comics"
        )

        self.create_config_dir("mylar")
        os.system("sudo usermod -a -G mediacenter mylar")

    # -----------------------------
    # Indexers
    # -----------------------------
    def prowlarr(self):
        ensure_user("prowlarr", 13006)
        self.create_config_dir("prowlarr")
        os.system("sudo usermod -a -G mediacenter prowlarr")

    def qbittorrent(self):
        ensure_user("qbittorrent", 13007)
        os.system("sudo usermod -a -G mediacenter qbittorrent")

    def jackett(self):
        ensure_user("jackett", 13008)
        self.create_config_dir("jackett")
        os.system("sudo usermod -a -G mediacenter jackett")

    def overseerr(self):
        ensure_user("overseerr", 13009)
        self.create_config_dir("overseerr")
        os.system("sudo usermod -a -G mediacenter overseerr")

    # -----------------------------
    # Media servers
    # -----------------------------
    def plex(self):
        ensure_user("plex", 13010)
        self.create_config_dir("plex")
        os.system("sudo usermod -a -G mediacenter plex")

    def sabnzbd(self):
        ensure_user("sabnzbd", 13011)
        self.create_config_dir("sabnzbd")
        os.system("sudo usermod -a -G mediacenter sabnzbd")

    def jellyseerr(self):
        ensure_user("jellyseerr", 13012)
        self.create_config_dir("jellyseerr")
        os.system("sudo usermod -a -G mediacenter jellyseerr")

    def bazarr(self):
        ensure_user("bazarr", 13013)
        self.create_config_dir("bazarr")
        os.system("sudo usermod -a -G mediacenter bazarr")

    def audiobookshelf(self):
        ensure_user("audiobookshelf", 13014)

        os.system(
            f"sudo mkdir -pv {self.root_dir_hdd}/data/media/{{audiobooks,podcasts,audiobookshelf-metadata}} -m 775"
            f" && sudo chown -R audiobookshelf:mediacenter {self.root_dir_hdd}/data/media/{{audiobooks,podcasts,audiobookshelf-metadata}}"
        )

        self.create_config_dir("audiobookshelf")
        os.system("sudo usermod -a -G mediacenter audiobookshelf")

    def plextraktsync(self):
        ensure_user("plextraktsync", 13015)
        self.create_config_dir("plextraktsync")
        os.system("sudo usermod -a -G mediacenter plextraktsync")

    def unpackerr(self):
        ensure_user("unpackerr", 13016)
        self.create_config_dir("unpackerr")
        os.system("sudo usermod -a -G mediacenter unpackerr")

    def recyclarr(self):
        ensure_user("recyclarr", 13017)

        os.system(
            f"sudo mkdir -p {self.root_dir_ssd}/config/recyclarr -m 775"
            f" && sudo chown -R recyclarr:mediacenter {self.root_dir_ssd}/config/recyclarr"
            f" && sudo chown $(id -u):mediacenter {self.root_dir_ssd}/config"
        )

    def cleanuparr(self):
        ensure_user("cleanuparr", 13018)
        self.create_config_dir("cleanuparr")

    def nginx_proxy_manager(self):
        ensure_user("nginx-proxy-manager", 13019)
        self.create_config_dir("nginx-proxy-manager")

    def adguardhome(self):
        ensure_user("adguardhome", 13020)
        self.create_config_dir("adguardhome")

    def cloudflared(self):
        ensure_user("cloudflared", 13021)
        self.create_config_dir("cloudflared")