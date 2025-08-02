import os

# UID up to 13017
class UserGroupSetup:
    def __init__(self, root_dir_ssd='/', root_dir_hdd='/'):
        self.root_dir_ssd = root_dir_ssd
        self.root_dir_hdd = root_dir_hdd
        os.system('sudo groupadd -g 13000 mediacenter || true')
        os.system('sudo usermod -a -G mediacenter $USER')
        os.system(
            '/bin/bash -c "'
            'sudo mkdir -pv -m 775 ' + self.root_dir_hdd + '/data/{media,usenet,torrents} '
            + self.root_dir_hdd + '/data/usenet/{incomplete,complete} '
            + self.root_dir_hdd + '/data/torrents/{incomplete,complete}'
            ' ; '
            'sudo chown -R $(id -u):mediacenter ' + self.root_dir_hdd + '/data'
            '"'
        )
    def create_config_dir(self, service_name):
        os.system(
            f'sudo mkdir -p {self.root_dir_ssd}/config/{service_name}-config -m 775'  # -m 775 gives read/write access to the whole mediacenter group
            f' ; sudo chown -R {service_name}:mediacenter {self.root_dir_ssd}/config/{service_name}-config'
            f' ; sudo chown $(id -u):mediacenter {self.root_dir_ssd}/config'
        )

    def sonarr(self):
        os.system(
            '/bin/bash -c "sudo useradd sonarr -u 13001'
            ' ; sudo mkdir -pv ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/{anime,cartoons,tv} -m 775'
            ' ; sudo chown -R sonarr:mediacenter ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/{anime,cartoons,tv}"'
        )
        self.create_config_dir('sonarr')
        os.system('sudo usermod -a -G mediacenter sonarr')


    def radarr(self):
        os.system(
            '/bin/bash -c "sudo useradd radarr -u 13002'
            ' ; sudo mkdir -pv ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/{anime_movies,cartoon_movies,documentaries,movies} -m 775'
            ' ; sudo chown -R radarr:mediacenter ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/{anime_movies,cartoon_movies,documentaries,movies}"'
        )
        self.create_config_dir('radarr')
        os.system('sudo usermod -a -G mediacenter radarr')

    def recyclarr(self):
        # Create the folder without '-config' suffix:
        os.system(
            f'sudo mkdir -p {self.root_dir_ssd}/config/recyclarr -m 775'
            f' ; sudo chown -R recyclarr:mediacenter {self.root_dir_ssd}/config/recyclarr'
            f' ; sudo chown $(id -u):mediacenter {self.root_dir_ssd}/config'
        )
        os.system('sudo useradd recyclarr -u 13017 || true')
        os.system('sudo usermod -a -G mediacenter recyclarr')


    def bazarr(self):
        os.system('/bin/bash -c "sudo useradd bazarr -u 13013"')
        self.create_config_dir('bazarr')
        os.system('sudo usermod -a -G mediacenter bazarr')

    def lidarr(self):
        os.system(
            '/bin/bash -c "sudo useradd lidarr -u 13003'
            ' ; sudo mkdir -pv ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/music -m 775'
            ' ; sudo chown -R lidarr:mediacenter ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/music"'
        )
        self.create_config_dir('lidarr')
        os.system('sudo usermod -a -G mediacenter lidarr')

    def readarr(self):
        os.system(
            '/bin/bash -c "sudo useradd readarr -u 13004'
            ' ; sudo mkdir -pv ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/books -m 775'
            ' ; sudo chown -R readarr:mediacenter ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/books"'
        )
        self.create_config_dir('readarr')
        os.system('sudo usermod -a -G mediacenter readarr')

    def mylar3(self):
        os.system(
            '/bin/bash -c "sudo useradd mylar -u 13005'
            ' ; sudo mkdir -pv ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/comics -m 775'
            ' ; sudo chown -R mylar:mediacenter ' + self.root_dir_hdd + '/data/{media,usenet,torrents}/comics"'
        )
        self.create_config_dir('mylar')
        os.system('sudo usermod -a -G mediacenter mylar')

    def audiobookshelf(self):
        os.system(
            '/bin/bash -c "sudo useradd audiobookshelf -u 13014'
            ' ; sudo mkdir -pv ' + self.root_dir_hdd + '/data/media/{audiobooks,podcasts,audiobookshelf-metadata} -m 775'
            ' ; sudo chown -R audiobookshelf:mediacenter ' + self.root_dir_hdd + '/data/media/{audiobooks,podcasts,audiobookshelf-metadata}"'
        )
        self.create_config_dir('audiobookshelf')
        os.system('sudo usermod -a -G mediacenter audiobookshelf')

    def prowlarr(self):
        os.system('sudo useradd prowlarr -u 13006')
        self.create_config_dir('prowlarr')
        os.system('sudo usermod -a -G mediacenter prowlarr')

    def qbittorrent(self):
        os.system('sudo useradd qbittorrent -u 13007')
        os.system('sudo usermod -a -G mediacenter qbittorrent')

    def overseerr(self):
        os.system('sudo useradd overseerr -u 13009')
        self.create_config_dir('overseerr')
        os.system('sudo usermod -a -G mediacenter overseerr')

    def plex(self):
        os.system('sudo useradd plex -u 13010')
        self.create_config_dir('plex')
        os.system('sudo usermod -a -G mediacenter plex')
    
    def plextraktsync(self):
        os.system('sudo useradd plextraktsync -u 13015')
        self.create_config_dir('plextraktsync')
        os.system('sudo usermod -a -G mediacenter plextraktsync')

    def unpackerr(self):
        os.system('sudo useradd unpackerr -u 13016')
        self.create_config_dir('unpackerr')
        os.system('sudo usermod -a -G mediacenter unpackerr')

    def sabnzbd(self):
        os.system('sudo useradd sabnzbd -u 13011')
        self.create_config_dir('sabnzbd')
        os.system('sudo usermod -a -G mediacenter sabnzbd')

    def jellyseerr(self):
        os.system('sudo useradd jellyseerr -u 13012')
        self.create_config_dir('jellyseerr')
        os.system('sudo usermod -a -G mediacenter jellyseerr')

    def jackett(self):
        os.system('sudo useradd jackett -u 13008')
        self.create_config_dir('jackett')
        os.system('sudo usermod -a -G mediacenter jackett')
