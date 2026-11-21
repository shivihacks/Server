# Server
Local server

# <div align="center">

# ShivShare LAN

**Offline Local Network File Sharing Tool for Android over Wi-Fi and Mobile Hotspot**

ShivShare LAN enables Android devices to transfer files over a local Wi-Fi network or mobile hotspot using Termux and Python on port `8080`, accessed through a web browser via the server device's local IP address without requiring an internet connection.

[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Termux-3DDC84?style=for-the-badge&logo=android&logoColor=white)](#installation-guide)
[![Runtime](https://img.shields.io/badge/Runtime-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#technology-stack)
[![Network](https://img.shields.io/badge/Network-Offline%20LAN%20%7C%20Port%208080-0F766E?style=for-the-badge)](#how-it-works)
[![License](https://img.shields.io/badge/License-Verify%20LICENSE%20File-64748B?style=for-the-badge)](#license)

[Overview](#hero-section) • [Features](#features) • [How It Works](#how-it-works) • [Installation](#installation-guide) • [Usage](#usage-guide) • [Structure](#project-structure) • [Troubleshooting](#troubleshooting) • [Roadmap](#roadmap)

</div>

---

## Hero Section

### What Is ShivShare LAN?

**ShivShare LAN** is an offline local-area-network file sharing tool designed to run on Android via **Termux** and **Python**. One Android device hosts a local HTTP server listening on port `8080`, and one or more client devices connect to that server from a web browser using the host device's local IPv4 address.

### Why Was It Created?

Transferring files between phones often relies on cloud storage services, messaging apps, or external internet access. In environments without mobile data or internet connectivity—or when moving large local files between devices on the same network—cloud workflows are slow, unavailable, or unnecessary.

### Problem It Solves

- **Works without internet access:** Transfers happen strictly over a local Wi-Fi network or mobile hotspot.
- **Avoids cloud intermediaries:** Files move directly between connected devices on the local network rather than uploading to and downloading from remote cloud servers.
- **Browser-based client access:** Connecting devices only need a modern web browser pointing to `http://<SERVER_IP>:8080`.

### How It Works

Instead of routing data through cloud storage, ShivShare LAN uses local TCP/IP networking on your Wi-Fi router or hotspot subnet. The server phone binds to port `8080` on its local network interface, and browser clients on the same subnet communicate directly with that local endpoint over HTTP.

---

## Features

> **Verification Note:** Only core project behavior described in the project specification is listed as established below. Confirm every specific UI and transfer capability directly against your source code before publishing, and keep unverified or incomplete capabilities marked as planned or in development.

### Confirmed / Core Capabilities

- **Offline File Transfer:** Transfers files over a local network without requiring internet access or cloud storage.
- **Local Wi-Fi & Hotspot Communication:** Operates across devices connected to the same Wi-Fi network or mobile hotspot.
- **Android Termux Support:** Built to run on Android inside the Termux terminal environment using Python.
- **Browser-Based Access (Port `8080`):** Serves a web interface on port `8080` reachable via the server device's local IP address.

### Pending Code Verification / In Development

Verify whether the following features exist in your current codebase before marking them complete:

- [ ] File upload and download endpoints
- [ ] Multiple file transfer support
- [ ] Real-time transfer progress indicator
- [ ] Transfer speed metrics
- [ ] Connected devices list / session view
- [ ] File management actions (browse, rename, delete, or organize files)
- [ ] Transfer history log
- [ ] PIN authentication / device authorization prompt

---

## Screenshots

Screenshots have not yet been captured or added to the repository. Once you capture interface views from a running session, save them under `docs/screenshots/` and update the alt text and captions as needed.

| View | Planned File Path | Description |
| :--- | :--- | :--- |
| Dashboard | `docs/screenshots/dashboard.png` | Main browser interface showing server status and quick transfer actions |
| File Manager | `docs/screenshots/file-manager.png` | Shared files view for browsing, uploading, or downloading files |
| Transfer Progress | `docs/screenshots/transfer-progress.png` | Active file transfer status view |
| Connected Devices | `docs/screenshots/connected-devices.png` | Devices connected to the local server session |

---

## How It Works

### Connection Workflow

1. **Install the project on the server phone:** Set up Termux, Python, required dependencies, and the ShivShare LAN repository on the host Android device.
2. **Connect both phones to the same Wi-Fi or mobile hotspot:** Join the same local network on both the server device and client device(s).
3. **Start the server using Termux:** Launch the ShivShare LAN Python application so it listens on port `8080`.
4. **Get the local IP address and port `8080`:** Find the server device's local IPv4 address on the active Wi-Fi/hotspot interface (for example, `192.168.x.x`) and combine it with port `8080`.
5. **Open the local URL in the second phone's browser:** Navigate to `http://<SERVER_IP>:8080` in the client device's browser.
6. **Authorize the device connection:** Complete any PIN or connection authorization step if enabled in your implementation.
7. **Select files and start transferring:** Choose files in the browser interface to upload or download across the local network.

### Architecture Diagram

```mermaid
flowchart LR
    subgraph LAN["Local Network (Wi-Fi / Mobile Hotspot — No Internet Required)"]
        subgraph ServerPhone["Server Android Device (Termux)"]
            ServerApp["ShivShare LAN Server<br/>Python HTTP Service (:8080)"]
            LocalStorage["Local Device Storage<br/>(/sdcard / Shared Folder)"]
            ServerApp <--> LocalStorage
        end

        subgraph ClientPhone["Client Android Device"]
            Browser["Web Browser<br/>http://&lt;SERVER_IP&gt;:8080"]
        end

        Browser <-->|"HTTP over Local IPv4:8080"| ServerApp
    end
