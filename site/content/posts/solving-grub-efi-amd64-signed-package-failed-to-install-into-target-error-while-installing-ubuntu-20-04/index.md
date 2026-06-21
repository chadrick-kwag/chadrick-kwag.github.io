---


title: solving "'grub-efi-amd64-signed' package failed to install into /target/."
  error while installing ubuntu 20.04
date: '2020-06-03T00:00:00+00:00'
lastmod: '2020-06-03T00:00:00+00:00'
slug: solving-grub-efi-amd64-signed-package-failed-to-install-into-target-error-while-installing-ubuntu-20-04
categories:
- linux
tags:
- "ubuntu"
- "grub-efi-amd64-signed-package-failed-to-install"
- "ubuntu-20-04-install"
- "solving"
- "grub"
draft: false
---
I encountered the infamous “'**grub**-**efi**-**amd64**-**signed**' **package failed to install into** /**target**/.” error when installing ubuntu 20.04 along with preinstalled windows 10 in my desktop. Here are the setting environments

- gigabyte mainboard
- one SSD, one HDD
- windows 10 already installed on SSD

I wanted to install ubuntu 20.04 on the HDD so I partitioned the HDD to have one EFI partition(500MB) and the rest set to ‘/’ with ext4 format.

I created a ubuntu 20.04 install usb stick using the image downloaded from the official ubuntu website and Rufus. At the time, I selected ‘BIOS or UEFI’ for “target system” option when creating the usb stick.

With the above settings, no matter what I do I always ended up with the same error at the last moment of the installation.

## Solution

After pouring over numerous googling results on this error and failing with all suggested solutions, I still managed to get out some sense of the situation.

And after a lot of fidgeting, I finally found my own solution.

In my case, the problem lied in the process of creating a booting usb stick. When using Rufus, I tried out **“UEFI(non CMS)"** for “target system” option instead of “BIOS or UEFI”.

Then I booted into the live usb stick and carried on with the same partitioning scheme as I did previously, and this time the installation did not give me the error.

BTW, although it said “(non CMS)” in the select option in Rufus, I still managed to boot into the usb stick even when CMS was enabled in my mainboard settings. I guess it actually meant that it doesn’t support legacy boot modes rather than “CMS must be disabled when booting to a usb stick created with this option!”.

My own understanding of why this method worked is that by creating a live usb stick with the “UEFI(non CMS)” option somehow forces the live usb stick to install ubuntu UEFI mode and not in legacy mode, which installs bootloader on MBR.

Previously when I used the “BIOS or UEFI” option, although the name gives a sense that both modes will be supported, I think it was actually working only on BIOS mode. Therefore, it was installing the boot loaders in legacy mode which did not abide well with the pre-existing windows 10 which was installed in UEFI mode.

My explanation may not be technically accurate, so don’t take my word for granted but as a supplementary advice.
