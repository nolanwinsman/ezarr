import os
import subprocess


# -----------------------------
# Helpers
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


def run(cmd):
    subprocess.run(cmd, check=True)


def ensure_user(username, uid):
    #if user_exists(username):
    #    print(f"[SKIP] user '{username}' already exists")
    #    return

    print(f"[CREATE] user '{username}' (uid {uid})")
    os.system(f"sudo useradd {username} -u {uid}")


def ensure_group(groupname, gid):
    #if group_exists(groupname):
    #    print(f"[SKIP] group '{groupname}' already exists")
    #    return

    print(f"[CREATE] group '{groupname}' (gid {gid})")
    os.system(f"sudo groupadd -g {gid} {groupname}")


# -----------------------------
# Main class
# -----------------------------
class UserGroupSetup:
    def __init__(self, root_dir_ssd='/', root_dir_hdd='/'):
        self.root_dir_ssd = root_dir_ssd
        self.root_dir_hdd = root_dir_hdd

        # NEW: proper permission separation
        ensure_group("media_read", 12999)
        ensure_group("media_write", 13000)

        # add current user to write group (for management)
        run(["sudo", "usermod", "-a", "-G", "media_write", os.getenv("USER")])

        media_root = f"{self.root_dir_hdd}/data"

        run([
            "sudo", "mkdir", "-pv", "-m", "775",
            f"{media_root}/media",
            f"{media_root}/usenet",
            f"{media_root}/torrents",
            f"{media_root}/usenet/incomplete",
            f"{media_root}/usenet/complete",
            f"{media_root}/torrents/incomplete",
            f"{media_root}/torrents/complete",
        ])

        # Ownership: write group controls filesystem writes
        run([
            "sudo", "chown",
            f"{os.getuid()}:media_write",
            media_root
        ])

    # -----------------------------
    # ARR STACK (WRITE ACCESS)
    # -----------------------------
    def sonarr(self):
        ensure_user("sonarr", 13001)

        os.system(
            "sudo usermod -a -G media_write sonarr"
        )

        self.create_config_dir("sonarr")

    def radarr(self):
        ensure_user("radarr", 13002)

        os.system(
            "sudo usermod -a -G media_write radarr"
        )

        self.create_config_dir("radarr")

    def lidarr(self):
        ensure_user("lidarr", 13003)

        os.system(
            "sudo usermod -a -G media_write lidarr"
        )

        self.create_config_dir("lidarr")

    def readarr(self):
        ensure_user("readarr", 13004)

        os.system(
            "sudo usermod -a -G media_write readarr"
        )

        self.create_config_dir("readarr")

    def mylar3(self):
        ensure_user("mylar", 13005)

        os.system(
            "sudo usermod -a -G media_write mylar"
        )

        self.create_config_dir("mylar")

    # -----------------------------
    # DOWNLOADERS (WRITE ACCESS)
    # -----------------------------
    def qbittorrent(self):
        ensure_user("qbittorrent", 13007)
        os.system("sudo usermod -a -G media_write qbittorrent")

    def sabnzbd(self):
        ensure_user("sabnzbd", 13011)
        self.create_config_dir("sabnzbd")
        os.system("sudo usermod -a -G media_write sabnzbd")

    def unpackerr(self):
        ensure_user("unpackerr", 13016)
        self.create_config_dir("unpackerr")
        os.system("sudo usermod -a -G media_write unpackerr")

    # -----------------------------
    # INDEXERS (NO MEDIA ACCESS)
    # -----------------------------
    def prowlarr(self):
        ensure_user("prowlarr", 13006)
        self.create_config_dir("prowlarr")

    def jackett(self):
        ensure_user("jackett", 13008)
        self.create_config_dir("jackett")

    # -----------------------------
    # MEDIA SERVERS
    # -----------------------------
    def plex(self):
        ensure_user("plex", 13010)
        self.create_config_dir("plex")

        # optional: read-only group if you use Plex too
        os.system("sudo usermod -a -G media_read plex")

    def jellyfin(self):
        ensure_user("jellyfin", 13022)
        self.create_config_dir("jellyfin")

        # ONLY read access
        os.system("sudo usermod -a -G media_read jellyfin")

    def jellyseerr(self):
        ensure_user("jellyseerr", 13012)
        self.create_config_dir("jellyseerr")
        # NO filesystem access required

    def overseerr(self):
        ensure_user("overseerr", 13009)
        self.create_config_dir("overseerr")

    def bazarr(self):
        ensure_user("bazarr", 13013)
        self.create_config_dir("bazarr")
        os.system("sudo usermod -a -G media_write bazarr")

    def audiobookshelf(self):
        ensure_user("audiobookshelf", 13014)

        os.system(
            f"sudo mkdir -pv {self.root_dir_hdd}/data/media/{{audiobooks,podcasts,audiobookshelf-metadata}} -m 775"
        )

        os.system("sudo usermod -a -G media_write audiobookshelf")
        self.create_config_dir("audiobookshelf")

    # -----------------------------
    # CONFIG HELPERS
    # -----------------------------
    def create_config_dir(self, service_name):
        os.system(
            f"sudo mkdir -p {self.root_dir_ssd}/config/{service_name}-config -m 775"
            f" && sudo chown -R {service_name}:media_write {self.root_dir_ssd}/config/{service_name}-config"
        )
