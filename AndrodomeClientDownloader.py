import requests
import wget
import os
import shutil
from zipfile import ZipFile

BaseUrl = "https://androdome.com/DeployHistory/version/version-"
Version = "fb3436d54f9e4598"

BaseFolder = "versions\\version-" + Version + "\\"
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

os.makedirs(BaseFolder, 511, True)

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

def main_function():
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
