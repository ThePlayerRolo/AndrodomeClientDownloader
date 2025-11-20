import argparse
import os
import shutil
from zipfile import ZipFile
import requests
import wget

BaseUrl = "https://androdome.com/DeployHistory/version/version-"
ContentFolder = "content\\"

AllZips = [
    "RobloxApp.zip",
    "RobloxStudio.zip",
    "RobloxPlayerLauncher.exe",
    "Roblox.exe",
    "redist.zip",
    "Libraries.zip",
    "imageformats.zip",
    "shaders.zip",
    "BuiltInPlugins.zip",
    "content-textures.zip",
    "content-textures2.zip",
    "content-textures3.zip",
    "content-fonts.zip",
    "content-music.zip",
    "content-sky.zip",
    "content-sounds.zip",
    "content-materials.zip",
    "content-particles.zip",
    "RobloxProxy.zip",
    "RobloxVersion.txt",
    "rbxManifest.txt",
    "NPRobloxProxy.zip"
]
NewDirectoryForZip = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "shaders\\",
    "BuiltInPlugins\\",
    ContentFolder + "textures\\",
    ContentFolder + "textures\\",
    ContentFolder + "textures\\",
    ContentFolder + "fonts\\",
    ContentFolder + "music\\",
    ContentFolder + "sky\\",
    ContentFolder + "sounds\\",
    ContentFolder + "materials\\",
    ContentFolder + "particles\\",
    "Extras\\",
    "Extras\\",
    "Extras\\",
    "Extras\\"
]

global Version
Version = ""
global BaseFolder
BaseFolder = ""

def checkIfUrlExists(urlString: str):
    request = requests.head(urlString, allow_redirects=True)
    return request.status_code == 200

def ExtractZip(baseFolder: str, nameOfZip: str, extraDir: str):
    finalDir = baseFolder + extraDir
    os.makedirs(finalDir, 511, True)
    texturesZip = ZipFile(baseFolder + nameOfZip, 'r')
    texturesZip.extractall(finalDir)
    texturesZip.close()
    os.remove(baseFolder + nameOfZip)

def getVersion():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Hash that represents the Roblox Version to Install")
    args = parser.parse_args()
    if args.version:
        return args.version
    return ""

def main_function():
    Version = getVersion()
    if Version == "":
        print("ERROR: -v must be provided!")
        exit()
    BaseFolder = "versions\\version-" + Version + "\\"
    os.makedirs(BaseFolder, 511, True)
    for i in range(len(AllZips)):
        urlString = BaseUrl + Version + "-" + AllZips[i]
        if (checkIfUrlExists(urlString)):
            print("Downloading " + urlString + "...\n")
            wget.download(urlString, BaseFolder)

            nameOfZip = "version-" + Version + "-" + AllZips[i]
            if ".zip" in nameOfZip:
                print("\nExtracting " + nameOfZip + "...\n")
                ExtractZip(BaseFolder, nameOfZip, NewDirectoryForZip[i])
            else:
                if ".exe" not in nameOfZip:
                    print("\nMoving " + BaseFolder + nameOfZip + " To " + NewDirectoryForZip[i])
                    shutil.move(BaseFolder + nameOfZip, BaseFolder + NewDirectoryForZip[i])
                print('\n')

    print("Copying AppSettings.xml ....\n")
    shutil.copyfile("AppSettings.xml", BaseFolder + "AppSettings.xml")
    print("Finished Copying AppSettings.xml!\n")
    print("Finished Downloading and Extracting Version " + Version + "!\n")


main_function()
