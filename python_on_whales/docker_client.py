import base64
from typing import List, Optional

from python_on_whales.client_config import ClientConfig, DockerCLICaller
from python_on_whales.components.buildx.cli_wrapper import BuildxCLI
from python_on_whales.components.compose.cli_wrapper import ComposeCLI
from python_on_whales.components.config.cli_wrapper import ConfigCLI
from python_on_whales.components.container.cli_wrapper import ContainerCLI
from python_on_whales.components.context.cli_wrapper import ContextCLI
from python_on_whales.components.image.cli_wrapper import ImageCLI
from python_on_whales.components.manifest.cli_wrapper import ManifestCLI
from python_on_whales.components.network.cli_wrapper import NetworkCLI
from python_on_whales.components.node.cli_wrapper import NodeCLI
from python_on_whales.components.plugin.cli_wrapper import PluginCLI
from python_on_whales.components.secret.cli_wrapper import SecretCLI
from python_on_whales.components.service.cli_wrapper import ServiceCLI
from python_on_whales.components.stack.cli_wrapper import StackCLI
from python_on_whales.components.swarm.cli_wrapper import SwarmCLI
from python_on_whales.components.system.cli_wrapper import SystemCLI
from python_on_whales.components.task.cli_wrapper import TaskCLI
from python_on_whales.components.trust.cli_wrapper import TrustCLI
from python_on_whales.components.volume.cli_wrapper import VolumeCLI

from .utils import ValidPath, run


class DockerClient(DockerCLICaller):
    """Creates a Docker client

    Note that
    ```python
    from python_on_whales import docker
    print(docker.run("hello-world"))
    ```
    is equivalent to
    ```python
    from python_on_whales import DockerClient
    docker = DockerClient()
    print(docker.run("hello-world")
    ```

    # Arguments
        config: Location of client config files (default "~/.docker")
        context: Name of the context to use to connect to the
            daemon (overrides DOCKER_HOST env var
            and default context set with "docker context use")
        debug: Enable debug mode
        host: Daemon socket(s) to connect to
        log_level: Set the logging level ("debug"|"info"|"warn"|"error"|"fatal")
           (default "info")
        tls:  Use TLS; implied by `tlsverify`
        tlscacert: Trust certs signed only by this CA (default "~/.docker/ca.pem")
        compose_files: Docker compose yaml file
        compose_env_file: .env file containing the environments variables to inject
            into the compose project. By default, it uses `./.env`.
    """

    def __init__(
        self,
        config: Optional[ValidPath] = None,
        context: Optional[str] = None,
        debug: Optional[bool] = None,
        host: Optional[str] = None,
        log_level: Optional[str] = None,
        tls: Optional[bool] = None,
        tlscacert: Optional[ValidPath] = None,
        tlscert: Optional[ValidPath] = None,
        tlskey: Optional[ValidPath] = None,
        tlsverify: Optional[bool] = None,
        client_config: Optional[ClientConfig] = None,
        compose_files: List[ValidPath] = [],
        compose_env_file: Optional[ValidPath] = None,
    ):

        if client_config is None:
            client_config = ClientConfig(
                config=config,
                context=context,
                debug=debug,
                host=host,
                log_level=log_level,
                tls=tls,
                tlscacert=tlscacert,
                tlscert=tlscert,
                tlskey=tlskey,
                tlsverify=tlsverify,
                compose_files=compose_files,
                compose_env_file=compose_env_file,
            )
        super().__init__(client_config)

        self.buildx = BuildxCLI(self.client_config)
        self.compose = ComposeCLI(self.client_config)
        self.config = ConfigCLI(self.client_config)
        self.container = ContainerCLI(self.client_config)
        self.context = ContextCLI(self.client_config)
        self.image = ImageCLI(self.client_config)
        self.manifest = ManifestCLI(self.client_config)
        self.network = NetworkCLI(self.client_config)
        self.node = NodeCLI(self.client_config)
        self.plugin = PluginCLI(self.client_config)
        self.secret = SecretCLI(self.client_config)
        self.service = ServiceCLI(self.client_config)
        self.stack = StackCLI(self.client_config)
        self.swarm = SwarmCLI(self.client_config)
        self.system = SystemCLI(self.client_config)
        self.task = TaskCLI(self.client_config)
        self.trust = TrustCLI(self.client_config)
        self.volume = VolumeCLI(self.client_config)

        # aliases
        self.attach = None
        self.build = self.buildx.build
        self.commit = self.container.commit
        self.copy = self.container.copy
        self.create = self.container.create
        self.diff = self.container.diff
        self.events = None
        self.execute = self.container.execute
        self.export = self.container.export
        self.images = self.image.list
        self.import_ = self.image.import_
        self.info = self.system.info
        # self.inspect -> too hard to implement
        self.kill = self.container.kill
        self.load = self.image.load
        self.logs = self.container.logs
        self.pause = self.container.pause
        self.ps = self.container.list
        self.pull = self.image.pull
        self.push = self.image.push
        self.rename = self.container.rename
        self.restart = self.container.restart
        self.remove = self.container.remove
        # self.rmi -> doesn't make much sense since it would be docker.remove_image
        self.run = self.container.run
        self.save = self.image.save
        # self.search -> Is anybody going to use it in python?
        self.start = self.container.start
        self.stats = self.container.stats
        self.stop = self.container.stop
        self.tag = self.image.tag
        self.top = self.container.stop
        self.unpause = self.container.unpause
        self.update = self.container.update
        self.wait = self.container.wait

    def version(self):
        """Not yet implemented"""
        raise NotImplementedError

    def login(
        self,
        server: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """Log in to a Docker registry.

        If no server is specified, the default is defined by the daemon.

        # Arguments
            server: The server to log into. For example, with a self-hosted registry
                it might be something like `server="192.168.0.10:5000"`
            username: The username
            password: The password
        """
        full_cmd = self.docker_cmd + ["login"]

        full_cmd.add_simple_arg("--username", username)
        full_cmd.add_simple_arg("--password", password)
        if server is not None:
            full_cmd.append(server)

        run(full_cmd, capture_stderr=False, capture_stdout=False)

    def logout(self, server: Optional[str] = None):
        """Logout from a Docker registry

        # Arguments
            server: The server to logout from. For example, with a self-hosted registry
                it might be something like `server="192.168.0.10:5000"`
        """
        full_cmd = self.docker_cmd + ["logout"]

        if server is not None:
            full_cmd.append(server)

        run(full_cmd, capture_stdout=False, capture_stderr=False)

    def login_ecr(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: Optional[str] = None,
    ):
        """Login to the aws ECR registry. Credentials are taken from the
        environment variables as defined in
        [the aws docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html).

        If you don't have a profile or your environment variables configured, you can also
        use the function arguments `aws_access_key_id`, `aws_secret_access_key`, `region_name`.

        Behind the scenes, those arguments are passed directly to
        ```python
        botocore.session.get_session().create_client(...)
        ```

        You need botocore to run this function. Use `pip install botocore` to install it.
        """
        import botocore.session

        client = botocore.session.get_session().create_client(
            "ecr",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

        response = client.get_authorization_token()["authorizationData"][0]
        credentials = base64.b64decode(response["authorizationToken"]).decode()
        username, password = credentials.split(":")
        registry = response["proxyEndpoint"]
        self.login(registry, username, password)
