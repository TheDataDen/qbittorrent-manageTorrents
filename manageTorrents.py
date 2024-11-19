from threading import Timer
from datetime import datetime, timedelta
import os
import sys
import qbittorrentapi
from qbittorrentapi import TorrentStates 

timer = None
tagName = 'not-managed'

# The qBitorrent WebUI needs to be enabled for this script to work
host = os.getenv('QBITTORRENT_HOST', '')
port = os.getenv('QBITTORRENT_PORT', '')
username = os.getenv('QBITTORRENT_USERNAME', '')
password = os.getenv('QBITTORRENT_PASSWORD', '')

# How often the port is checked in seconds
updateTime = os.getenv('QBITTORRENT_UPDATE_TIME_SECONDS', 120)

stalled = {}

def log(message):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(message))
    
def add_or_inc_stalled(hash):
    global stalled
    if hash in stalled:
        stalled[hash] += 1
    else:
        stalled[hash] = 1
        
def remove_from_stalled(hash):
    global stalled
    if hash in stalled:
        del stalled[hash]
        
def is_moved_to_bottom(hash):
    global stalled
    return hash in stalled and stalled[hash] == 1

def is_stalled(hash):
    global stalled
    return hash in stalled and stalled[hash] > 1

def auth_qbt():
    qbt_client = qbittorrentapi.Client(
        host=host, port=port, username=username, password=password)
    
    try:
        qbt_client.auth_log_in()
        log("Logged into qBittorrent!")
    except:
        e = sys.exc_info()[0]
        log("Error: %s" % e)
        log("qBittorrent probably isn't running or the credentials are incorrect.")
        log(host)
        log(port)
        log(username)
        log(password)
        sys.exit()
        
    return qbt_client
        
def get_torrents():
    qbt_client = auth_qbt()
    return qbt_client.torrents.info()

def move_torrent_to_bottom(hash):
    qbt_client = auth_qbt()
    qbt_client.torrents_bottom_priority(hash)
    
def delete_torrent(hash):
    qbt_client = auth_qbt()
    qbt_client.torrents_delete(True, hash)
    
def create_tag_if_not_exists():
    qbt_client = auth_qbt()
    
    existing_tags = qbt_client.torrents_tags()
    
    if tagName not in existing_tags:
        qbt_client.torrents_add_tag(tagName)
        log(f"Created tag {tagName}")
        
def run():
    torrents = get_torrents()
    manageable_torrents = [torrent for torrent in torrents if tagName not in torrent['tags']]
    
    for torrent in manageable_torrents:
        torrent_status = TorrentStates(torrent['state'])
        torrent_hash = torrent['hash']
        
        if torrent_status == TorrentStates.STOPPED_UPLOAD:
            state_changed_time = datetime.fromtimestamp(torrent.completion_on)
            time_in_state = datetime.now() - state_changed_time
            
            if time_in_state > timedelta(days=1):
                log(f"{torrent_hash} has been completed for over a day, deleting")
                delete_torrent(torrent_hash)
                continue
        
        if ((torrent_status == TorrentStates.STALLED_DOWNLOAD or torrent_status == TorrentStates.METADATA_DOWNLOAD) and torrent.priority <= 5):
            if is_moved_to_bottom(torrent_hash):
                log(f"{torrent_hash} marked as stalled")
                add_or_inc_stalled(torrent_hash)
                move_torrent_to_bottom(torrent_hash)
            elif is_stalled(torrent_hash):
                log(f"{torrent_hash} deleted")
                remove_from_stalled(torrent_hash)
                delete_torrent(torrent_hash)
            else:
                log(f"{torrent_hash} marked as moved to bottom")
                add_or_inc_stalled(torrent_hash)
                move_torrent_to_bottom(torrent_hash)
    
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def main():
    global timer
    
    if not host or not port or not username or not password:
        log("Missing environment variables. Please set the following variables:")
        log("QBITTORRENT_HOST")
        log("QBITTORRENT_PORT")
        log("QBITTORRENT_USERNAME")
        log("QBITTORRENT_PASSWORD")
        sys.exit()
    
    run()
    timer = RepeatedTimer(int(updateTime), run)

if __name__ == "__main__":
    main()