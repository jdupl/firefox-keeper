# firefox-keeper
Archives all your firefox bookmarks web pages to an external server.

# Client
The client reads saved bookmarks in `.mozilla` and sends them to the server.

# Server
Archives the bookmarks with plug-ins.

## Server plug-ins
* Default: Archive whole web page with wget
* Youtube: Archive video with youtube-dl
