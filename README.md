# 1password-export

1Password is a valuable and easy-to-use tool to store your credentials
in one place. These are safely stored in cloud services provided by
1Password. As with all cloud services, you are advices to periodically
make your own backup copies in case of an emergency. That is why this
tools exists. It creates an export of all your 1Password data into a
local folder of your choosing.

## Installation

The Python script `1password-export.py` requires:
* Python 3
* 1Password CLI integration

See https://developer.1password.com/docs/cli/ to setup 1Password CLI
integration. It works best with 1Password 8.

## Preparations

In order to create a safe export of your 1Password credentials, you need
to make sure that the data is exported into an encrypted folder only
accessible to you.

On a Mac you can use a secure disk image for this.
See https://support.apple.com/en-gb/guide/disk-utility/dskutl11888/mac
section 'Create a secure disk image' for instructions.

This guide assumes you created a secure disk image called 'Secure' which
has been mounted as '/Volumes/Secure'.

## Run

When you call the script with:

`python3 1password-export.py /Volumes/Secure/1password/export`

it will check if the specified directory does not already exist. If it
does, the script will abort with an error message. Next it will create
the export directory, and it will try to sign-in to your 1Password account
using the 1Password CLI tool. After a successful sign-in, it will create
a folder for each vault you have access to and export all items and documents
in that vault.

You can also specify a specific vault as an extra argument to the script.
