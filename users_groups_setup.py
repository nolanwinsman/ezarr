import os
import subprocess


# -----------------------------
# Helpers
# -----------------------------
def run(cmd):
    subprocess.run(cmd, check=True)


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


def get_uid(username):
    try:
        return int(subprocess.check_output(["id", "-u", username]).decode().strip())
    except:
        return None


# -----------------------------
# User / Group Management
# -----------------------------
def ensure_user(username, uid):
    current_uid = get_uid(username)

    if current_uid is None:
        print(f"[CREATE] user '{username}' (uid {uid})")
        run(["sudo", "useradd", "-u", str(uid), username])
        return

    print(f"[SKIP] user '{username}' exists")

    if current_uid != uid:
        print(f"[MIGRATE] UID change {current_uid} → {uid}")

        run(["sudo", "usermod", "-u", str(uid), username])

        # FIX ownership of old UID files (SAFE scoped)
        run([
            "sudo", "find", "/mnt",
            "-uid", str(current_uid),
            "-exec", "chown", "-h", username, "{}", "+"
        ])


def ensure_group(groupname, gid):
    existing = subprocess.run(
        ["getent", "group", str(gid)],
        capture_output=True,
        text=True
    ).stdout.strip()

    if existing:
        name = existing.split(":")[0]

        if name != groupname:
            raise Exception(f"GID {gid} already used by '{name}'")

        print(f"[SKIP] group '{groupname}' exists")

        run(["sudo", "groupmod", "-g", str(gid), groupname])

    else:
        print(f"[CREATE] group '{groupname}' (gid {gid})")
        run(["sudo", "groupadd", "-g", str(gid), groupname])


# -----------------------------
# Main Class
# -----------------------------
class UserGroupSetup:
    def __init__(self, root_dir_ssd='/', root_dir_hdd='/'):
        self.root_dir_ssd = root_dir_ssd
        self.root_dir_hdd = root_dir_hdd

        ensure_group("media_read", 12999)
        ensure_group("media_write", 13000)

        run([
            "sudo", "usermod",
            "-a", "-G", "media_write",
            os.getenv("USER")
        ])

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

        run([
            "sudo", "chown",
            f"{os.getuid()}:media_write",
            media_root
        ])

    # -----------------------------
    # Permission Helper (NEW)
    # -----------------------------
    def apply_media_access(self, user, access_type):
        if access_type == "read":
            run(["sudo", "usermod", "-a", "-G", "media_read", user])

        elif access_type == "write":
            run(["sudo", "usermod", "-a", "-G", "media_write", user])
            run(["sudo", "usermod", "-a", "-G", "media_read", user])

    # -----------------------------
    # ARR STACK
    # -----------------------------
    def sonarr(self):
        ensure_user("sonarr", 13001)
        self.apply_media_access("sonarr", "write")
        self.create_config_dir("sonarr")

    def radarr(self):
        ensure_user("radarr", 13002)
        self.apply_media_access("radarr", "write")
        self.create_config_dir("radarr")

    def lidarr(self):
        ensure_user("lidarr", 13003)
        self.apply_media_access("lidarr", "write")
        self.create_config_dir("lidarr")

    def readarr(self):
        ensure_user("readarr", 13004)
        self.apply_media_access("readarr", "write")
        self.create_config_dir("readarr")

    def mylar3(self):
        ensure_user("mylar", 13005)
        self.apply_media_access("mylar", "write")
        self.create_config_dir("mylar")

    # -----------------------------
    # DOWNLOADERS
    # -----------------------------
    def qbittorrent(self):
        ensure_user("qbittorrent", 13007)
        self.apply_media_access("qbittorrent", "write")

    def sabnzbd(self):
        ensure_user("sabnzbd", 13011)
        self.apply_media_access("sabnzbd", "write")
        self.create_config_dir("sabnzbd")

    def unpackerr(self):
        ensure_user("unpackerr", 13016)
        self.apply_media_access("unpackerr", "write")
        self.create_config_dir("unpackerr")

    # -----------------------------
    # INDEXERS
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
        self.apply_media_access("plex", "read")
        self.create_config_dir("plex")

    def jellyfin(self):
        ensure_user("jellyfin", 13022)
        self.apply_media_access("jellyfin", "read")
        self.create_config_dir("jellyfin")

    def jellyseerr(self):
        ensure_user("jellyseerr", 13012)
        self.create_config_dir("jellyseerr")

    def overseerr(self):
        ensure_user("overseerr", 13009)
        self.create_config_dir("overseerr")

    def bazarr(self):
        ensure_user("bazarr", 13013)
        self.apply_media_access("bazarr", "write")
        self.create_config_dir("bazarr")

    def audiobookshelf(self):
        ensure_user("audiobookshelf", 13014)

        run([
            "sudo", "mkdir", "-pv",
            f"{self.root_dir_hdd}/data/media/audiobooks",
            f"{self.root_dir_hdd}/data/media/podcasts"
        ])

        self.apply_media_access("audiobookshelf", "write")
        self.create_config_dir("audiobookshelf")

    # -----------------------------
    # CONFIG
    # -----------------------------
    def create_config_dir(self, service_name):
        run([
            "sudo", "mkdir", "-p",
            f"{self.root_dir_ssd}/config/{service_name}-config"
        ])

        run([
            "sudo", "chown",
            f"{service_name}:media_write",
            f"{self.root_dir_ssd}/config/{service_name}-config"
        ])