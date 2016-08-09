from os import path
import libtorrent
import shutil
from time import sleep

link=str(raw_input());
target_dir=path.abspath(".");
session=libtorrent.session();
params={
'save_path':target_dir,
'duplicate_is_error':True,
'storage_mode':libtorrent.storage_mode_t(2),
'paused':False,
'auto_managed':True
}
handle=libtorrent.add_magnet_uri(session,link,params);
print('trying.....')
while (not handle.has_metadata()):
#    try:
#        sleep(2);
	pass
#        print('wait')
"""    except KeyboardInterrupt:
        print("exiting");
        exit(0);"""
torinfo=handle.get_torrent_info();
torfiles=handle.files();
print('this it the infomation of this magnet link:\n')
print("Name:\n")
print(torinfo.name())
print("contents:")
for singlefile in torfiles:
    print(singlefile.path+"    "+singlefile.size)
