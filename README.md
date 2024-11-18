# qbittorrent-manageTorrents

A Docker container to help manage qBittorrent slow or dead torrents.

## Links

- [Docker Hub](https://hub.docker.com/r/strenkml/qbittorrent-manage-torrents)
- [GitHub](https://github.com/TheDataDen/qbittorrent-manageTorrents)

## Usage

### Docker Compose

1. Clone this repository:

```bash
git clone https://github.com/TheDataDen/qbittorrent-manageTorrents.git
cd qbittorrent-manageTorrents
```

2. Edit the `docker-compose.yml` file to set the environment variables and volumes as needed. Check the [Configuration](#configuration) section for more details.

3. Run the container:

```bash
docker-compose up -d
```

> [!NOTE]
> If you are running qBittorrent in a docker container (like qBittorrent-nox) you can add this container to your existing docker-compose.yml file.

### Docker Run

```bash
docker run -d \
  --name qbittorrent-manage-torrents \
  --restart unless-stopped \
  -e QBITTORRENT_HOST=127.0.0.1 \
  -e QBITTORRENT_PORT=8080 \
  -e QBITTORRENT_USERNAME=admin \
  -e QBITTORRENT_PASSWORD=adminadmin \
  -e QBITTORRENT_UPDATE_TIME_SECONDS=120 \
  strenkml/qbittorrent-manage-torrents
```

### Pull the Image

```bash
docker pull strenkml/qbittorrent-manage-torrents
```

## Configuration

### Environment Variables

The container can be configured using the following environment variables:

| Variable Name                     | Required | Default | Description                                      |
| --------------------------------- | -------- | ------- | ------------------------------------------------ |
| `QBITTORRENT_HOST`                | Yes      |         | Hostname or IP address of the qBittorrent WebUI. |
| `QBITTORRENT_PORT`                | Yes      |         | Port of the qBittorrent WebUI.                   |
| `QBITTORRENT_USERNAME`            | Yes      |         | Username of the qBittorrent WebUI.               |
| `QBITTORRENT_PASSWORD`            | Yes      |         | Password of the qBittorrent WebUI.               |
| `QBITTORRENT_UPDATE_TIME_SECONDS` | No       | `120`   | How often the torrent check runs                 |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue in this repository.
