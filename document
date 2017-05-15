
SYNOPSIS:

    amz [ options ] [ value ... ]
        [ -r -run ] [ -d -detail ] [ -u -user ] [ username ] alias image-id
        [ -f -find ] query
        [ -s -start ] [ ALL | instances-id ... | instances-alias ... ] 
        [ -S -stop ] [ ALL | instances-id ... | instances-alias ... ]
        [ -t -terminate ] [ ALL | instances-id ... | instances-alias ... ]
        [ -c -command ] command [ instance-id | instances-alias ] 
        [ -key-path ] path

DESCRIPTION:

    AMZ will make a new folder named .amz under users home directory. All information about instances and images will be stored there.
    This program will modify ~/.ssh/config file, it assumes the format in this file is:

    Host foo:
        User ubuntu
        HostName bar
        IdentityFile ~/ssh/your/key/path

OPTIONS:

        -r -run:
            Take an image-id as value and try to run this instance by defualt settings.
            If -d is specified, awz will ask for more detailed information about running this new instance.
            If -a is specified, an instances-alias is required for referencing this new instance.
            if -u is specified, an user name is required to be provied to login with ssh, the default value is "root"

        -f -find:
            Take an query as value, query support wildcard syntax. It will search for images with the query name provided.

        -s -start:
            Start instances that has been previously stopped.

        -S -stop:
            Take instance-ids or instance-aliases as values and stop it.
            Special value ALL for stop all instances in current region.

        -t -terminate:
            Take instance-ids or instance-aliases as values and terminate it.
            Special value ALL for terminate all instances in current region.

        -c -command:
            ls: list all running instances.
            cat:  get detailed information about an instance. Take a instance-id or instance-alias as input value.

        -key-path:
            Set defualt absolute key path to start a new instance.
