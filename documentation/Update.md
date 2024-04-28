# koalixcrm Update from V1.12 to V1.14

<b>Important:</b> This guide is specifically tailored to guide you through the update process from version V1.12 to V1.14. 
Other version migrations may not work with this guidance or may behave differently.

## Support

Just like the installation, a certain expertise in server administration is needed to update koalixcrm. 
For questions or support, please refer to our website http://www.koalix.com, where you can find more information about our services.

## Limitations

This update functionality is written exclusively for the transition from V1.12 to V1.14. It has not been tested 
for other version migrations, and the functionality is not guaranteed for such cases. Make sure you're updating from 
a properly tagged version (V1.12) to another tagged version (V1.14), and refrain from using the master branch for this process.

<b>Warning: The update from V1.12 to V1.14 might result in changes to your system. It's always recommended to backup 
your data before proceeding.</b>

## Before you update

It's strongly recommended that you backup both your koalixcrm project folder and your database before proceeding with
the update, because the process might introduce changes that would be irreversible otherwise.

# Update process

## Backup database and KoalixCRM

Backup your current database Backup your existing koalixcrm project folder

## Install Docker

In version V1.14, we are transitioning to Docker for smoother operation. Therefore, Docker must be installed before the
update. You can follow the Docker official documentation for the installation guide.

## Setup the new container

Once Docker is installed, go to https://github.com/KoalixSwitzerland/koalixcrm-prod-container and clone the repository.

## Edit Docker-compose file

Navigate into the cloned repository and open the docker-compose file. Update the settings according to your system.

## Restore your files and database from your backup

After setting up the new container and configuring the Docker-compose file, it's time to restore your files and the 
database from your backups you made earlier.

## Run the container

Now run the following command in your terminal:

'''docker-compose up'''

With this, your koalixcrm application should now be updated from V1.12 to V1.14 and running in the new Docker container.

Enjoy using KoalixCRM!
