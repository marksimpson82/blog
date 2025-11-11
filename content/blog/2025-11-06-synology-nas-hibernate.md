---
title: "Making my Synology DS224+ NAS hibernate"
date: 2025-11-06T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - dsm
  - synology
  - nas
---

## My old setup: Intel NUC, Jellyfin and a Roku stick
I've run an Intel NUC with the [Open Media Vault (OMV)](https://en.wikipedia.org/wiki/OpenMediaVault) distro and an external USB HDD since 2022. For my media server software, I started out with Plex and used it for a few years, but ultimately tired of the constant drip of stealthy on-by-default social features, live TV and so on. I swapped from Plex to Jellyfin and have been very happy with my choice. Jellyfin feels like a much more pleasant experience where my preferences are respected.

The final piece in the puzzle was a Roku 4k stick which meant I could disconnected my smart TV from the Internet. The Roku stick has superior Wi-Fi connectivity which meant I could ditch another Ethernet cable. While I do have concerns about Roku's business ethics and approach to data collection, it's better than relying on my archaic LG smart TV with its laggy interface and frequent crashes.

The NUC hardware was capable for transcoding, but I wasn't having much fun on a few fronts:
1. Maintaining the OMV install (a bit of a, "don't touch it" situation due to the configuration via GUIs)
2. The NUC's limited connectivity options meant I was in a bit of a storage dead-end. 

In short, I had a media PC with no Network Addressable Storage. My options were:
1. Buy a Direct Attached Storage (DAS) solution and run the NUC 24/7, turning it into a combination of poor man's NAS and a media server
2. Buy a Network Addressable Storage (NAS), but retain the NUC as a dedicated media server
3. Buy a dedicated NAS and run the media server software on it

I chose option 3, meaning I could retire my NUC.

## Moving to the DS224+ NAS
I purchased a Synology DS224+ NAS and chucked a second-hand `WD HUH721212ALE600` 12TB drive in it on account of [its excellent longevity](https://www.backblaze.com/blog/backblaze-drive-stats-for-q2-2025/) record (I also added a 12TB drive into my desktop PC for backup).

The DS224+ hardware is expensive for what it is, but it's sufficient to run Jellyfin and direct-play 1080p x265/HEVC media.

### Hardware and performance
The hardware does struggle with transcoding at higher resolutions, but I avoid this by:
1. Favouring 1080p HEVC media
2. Using bog-standard [SubRip](https://en.wikipedia.org/wiki/SubRip) subtitles

If you want to play 4k media, use PGS subtitles or transcode from other formats, I would recommend beefier hardware and/or a dedicated media server. E.g., when I tried to play a 4k AV1 file, it resulted in a locked system and then an error message. Oops!

### Adding cheap, unofficial RAM
The DS224+ comes with a meagre 2GB of RAM. I added another 4GB via [Mr. Memory](https://www.mrmemory.co.uk/memory-ram-upgrades/synology/nas/ds224_) for £13 rather than the obscene official Synology RAM prices (£92 at the time of writing!) 

**Note**: While the official documents claim that 4GB is the maximum supported DIMM size, various posts on reddit claim that larger DIMMS will work.

### The Synology OS: DiskStation Manager (DSM)
Synology devices use [DSM](https://en.wikipedia.org/wiki/Synology#DiskStation_Manager): a Linux-derived OS that's chiefly configured via web browser (depending on your preferences, this is either a pro or a con). While you can ssh into your NAS, don't expect to find everything you expect from a Linux distro. E.g. when I was debugging the lack of hibernation, many standard unix tools were missing.

### DSM's file browsing and shares are a bit weird
DSM has a package called `File Station` where you can browse your files. However, when you've got multiple drives and volumes, the association between volumes and folders/files is hidden. This information is available via right-clicking a file/folder and choosing "properties", but it's tucked away out of view.

To create a shared folder and choose the containing volume, you need to browse to `Control Panel` > `Shared Folder`.

E.g. I have a few shared folders set up as follows:

| Name | Volume | Description |
| ---- | ------ | ----------- |
| Media | Volume 1 (12TB IDE) | Media files (TV Shows, Films, Music) | 
| Docker | Volume 2 (400GB SSD) | Docker config, image files, jellyfin config etc |

### Adding an SSD
The DS224+ has two drive bays. I had an old 400GB SSD laying around, so I installed it as a second drive. My thinking was, "let's move the OS and packages onto the SSD to reduce the disk chuntering", but DSM doesn't work like that. 

Certain parts of the OS and its base packages are installed on all volumes. This is done for good reason: it means you can swap disks in and out, and you won't brick the OS.

You can see the installation location of packages via browsing to `Package Center` > `Installed` and selecting a package. Base packages will be listed as, "Installed volume: System partition".

However, you _can_ make your SSD the default installation location for custom packages to reduce the usage of your fatter, noisier disks. This is under `Package Center` > `Settings` > `Default Volume`.

I would strongly advise getting your drive/volume choices sorted out before you install and configure packages, as while tutorials exist for migrating packages between volumes, it's not fool-proof or comprehensive. DSM uses symlinks for various pieces of configuration and it's easy to break.

If you do find yourself needing to move packages between volumes, I would recommend doing the following:

1. Back up the configuration data
2. Manually uninstall the package from the old volume
3. Re-install the package on the new volume
4. Restore the configuration data to the new volume

Like I said, it's much easier to get your volumes and their purpose configured up-front and save yourself the hassle.

### Installing Jellyfin
Installing Jellyfin was straightforward:

1. Using `Control Panel` > `Shared Folder`, create shares for docker and your media on the appropriate volumes (already covered above)
1. Install and Open [Container Manager](https://www.synology.com/en-br/dsm/feature/docker)
1. Click the `Projects` tab
1. Add a project called "Jellyfin", and the path should be using the fastest/quietest drive volume (for me: `/volume2/docker/jellyfin`)
1. Add a docker-compose.yaml (while you can naively just start a container based on the `jellyfin/jellyfin` image, there's a load of implicit config involved that won't be reproducible -- better to just use a docker-compose file from the start).

A sample docker-compose file:

```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    healthcheck:
      # disable health check to avoid excess disk activity
      disable: true
    ports:
      # standard ports
      - 8096:8096/tcp
      - 7359:7359/udp
    volumes:
      # config & cache uses a fast/quiet SSD if possible
      - /volume2/docker/jellyfin/config:/config:rw
      - /volume2/docker/jellyfin/cache:/cache:rw
      # media is stored on my fat 12TB spinning rusk disk
      - type: bind
        source: /volume1/media
        target: /media
        read_only: true
    restart: 'unless-stopped'    
```

### Fixing Hibernation
There was one fly in the ointment: my DS224+ refused to hibernate, and this seems to be a common problem. My intial install used the 12TB IDE disk for everything, and it's _loud_. Not good.

Also, with all drives running, we're probably talking an extra 10-15W of power usage 24/7. At 25p/KWh that adds up to £2-3 per month, plus the extra wear and tear on the drives.

I started working through the [official documentation / checklist of items that may prevent hibernation](https://kb.synology.com/en-uk/DSM/tutorial/What_stops_my_Synology_NAS_from_entering_System_Hibernation) but it's a bit of a kitchen sink affair.

Here's what worked for me (though your mileage may vary):
1. Move packages (ContainerManager) and config (Docker) to my SSD
1. Disable Jellyfin's docker healthcheck via `healthcheck: disable`
1. Stop all non-essential packages
1. Disable the SSH service via `Control Panel` > `Terminal & SNMP` > `Terminal` > uncheck `Enable SSH Service`
1. Disable the bonjour service via `Control Panel` > `File Services` > `Bonjour` > uncheck `Enable Bonjour`
1. Unmap any network drives (I had my NAS mapped via my desktop PC)
1. Configure tasks to run less frequently via this [reddit thread](https://www.reddit.com/r/synology/comments/10cpbqd/making_disk_hibernation_work_on_synology_dsm_7/) (I moved some of the daily tasks to run weekly and stopped there).

After running through these steps, my NAS now hibernates after idling for a while. Success!

**Note**: It _does_ take ~30 seconds to wake up and become interactive. If that's too sluggish for you, then maybe just leave it running 24/7.
