import os

def create_file(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def create_service_structure(base_path, service_name):
    service_path = os.path.join(base_path, "services", service_name)
    files = {
        os.path.join(service_path, "__init__.py"): "# Init do pacote\n",
        os.path.join(service_path, "auth.py"): "",
        os.path.join(service_path, "config.py"): "",
        os.path.join(service_path, "Dockerfile"): (
            "FROM python:3.10-slim\n"
            "WORKDIR /app\n"
            "COPY . .\n"
            "RUN pip install -r requirements.txt\n"
            "CMD [\"python\", \"main.py\"]\n"
        ),
        os.path.join(service_path, "main.py"): (
            "if __name__ == '__main__':\n"
            "    print('Hello from main')\n"
        ),
        os.path.join(service_path, "requirements.txt"): "# Add dependencies here\n",
        os.path.join(service_path, "model", ".gitkeep"): "",
    }

    for file_path, content in files.items():
        create_file(file_path, content)

def generate_docker_compose(base_path, services):
    compose_header = "version: '3.8'\n\nservices:\n"
    networks = "networks:\n  backend:\n    driver: bridge\n"

    # Compose padrão
    base = ""
    for service in services:
        base += (
            f"  {service}:\n"
            f"    build: ./services/{service}\n"
            f"    container_name: {service}\n"
            f"    env_file: .env\n"
            f"    volumes:\n"
            f"      - ./services/{service}:/app\n"
            f"    networks:\n"
            f"      - backend\n\n"
        )

    # Compose dev
    dev = ""
    for service in services:
        dev += (
            f"  {service}:\n"
            f"    build: ./services/{service}\n"
            f"    container_name: {service}-dev\n"
            f"    environment:\n"
            f"      - LOG_LEVEL=DEBUG\n"
            f"    env_file: .env\n"
            f"    volumes:\n"
            f"      - ./services/{service}:/app\n"
            f"      - ./services:/app/services\n"
            f"      - ./videos:/app/videos\n"
            f"      - ./outputs:/app/outputs\n"
            f"      - ./tests:/app/tests\n"
            f"    networks:\n"
            f"      - backend\n"
            f"    entrypoint: [\"/bin/bash\", \"-c\"]\n"
            f"    command: [\"echo '🧪 Modo DEV ativo com log extendido' && python main.py\"]\n\n"
        )

    # Compose prd
    prd = ""
    for service in services:
        prd += (
            f"  {service}:\n"
            f"    image: registry.gitea.seuservidor.com/seu-usuario/{service}:latest\n"
            f"    container_name: {service}\n"
            f"    restart: unless-stopped\n"
            f"    env_file: .env.prd\n"
            f"    volumes:\n"
            f"      - ./services/{service}:/app\n"
            f"    networks:\n"
            f"      - backend\n\n"
        )

    create_file(os.path.join(base_path, "docker-compose.yaml"), compose_header + base + networks)
    create_file(os.path.join(base_path, "docker-compose.dev.yaml"), compose_header + dev + networks)
    create_file(os.path.join(base_path, "docker-compose.prd.yaml"), "# version: '3.8'\n\nservices:\n" + prd + networks)


def generate_makefile(base_path, services):
    base = (
        "# Variáveis configuráveis\n"
        "include .env\nexport\n\n"
        "ID ?= 1\n"
        "REGISTRY = registry.gitea.seuservidor.com\n"
        "USER = seu-usuario\n"
        f"IMAGE_NAME = $(REGISTRY)/$(USER)/{services[0]}\n"
        "TAG = latest\n\n"
        "COMPOSE = docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml --env-file .env\n\n"
        "up:\n\t$(COMPOSE) up --build -d\n"
        "down:\n\t$(COMPOSE) down -v\n"
        "prd-up:\n\tdocker-compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd up -d\n"
        "prd-down:\n\tdocker-compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd down -v\n\n"
    )

    for service in services:
        base += (
            f"restart-{service}:\n\t$(COMPOSE) restart {service}\n\n"
            f"redo-{service}:\n"
            f"\t$(COMPOSE) stop {service}\n"
            f"\t$(COMPOSE) rm -f {service}\n"
            f"\t$(COMPOSE) build {service}\n"
            f"\t$(COMPOSE) up -d {service}\n\n"
            f"logs-{service}:\n\t$(COMPOSE) logs -f {service}\n\n"
            f"prdlogs-{service}:\n"
            f"\tdocker-compose -f docker-compose.yaml -f docker-compose.prd.yaml --env-file .env.prd logs -f {service}\n\n"
            f"build-prd-{service}:\n\tdocker build -t $(IMAGE_NAME):$(TAG) ./services/{service}\n\n"
            f"push-gitea-{service}: build-prd-{service}\n\tdocker push $(IMAGE_NAME):$(TAG)\n\n"
        )

    base += (
        "local-tests: test-unit test-integration\n"
        "test-unit:\n\tPYTHONPATH=. pytest tests/unit --disable-warnings -v\n"
        "test-integration:\n\tPYTHONPATH=. pytest tests/integration --disable-warnings -v\n"
    )

    create_file(os.path.join(base_path, "Makefile"), base)

def create_project_structure(project_root, service_names):
    dirs = [
        "outputs",
        "tests",
        "tests/integration",
        "tests/unit",
        "services"
    ]
    files = [
        ".env",
        ".env.prd",
        ".gitignore",
        "pytest.ini",
        "README.md",
        "services/__init__.py"
    ]

    for d in dirs:
        os.makedirs(os.path.join(project_root, d), exist_ok=True)

    for f in files:
        create_file(os.path.join(project_root, f), "")

    for name in service_names:
        create_service_structure(project_root, name)

    generate_docker_compose(project_root, service_names)
    generate_makefile(project_root, service_names)

if __name__ == "__main__":
    project_root = input("Digite o nome da pasta raiz do projeto: ").strip()
    if not project_root:
        print("❌ Nome inválido. Saindo...")
        exit()

    try:
        num_services = int(input("Quantos serviços deseja criar? "))
    except ValueError:
        print("❌ Número inválido. Saindo...")
        exit()

    service_names = []
    for i in range(num_services):
        name = input(f"Digite o nome do service {i + 1}: ").strip()
        if name:
            service_names.append(name)
        else:
            print("❌ Nome de serviço vazio. Saindo...")
            exit()

    os.makedirs(project_root, exist_ok=True)
    create_project_structure(project_root, service_names)

    print(f"\n✅ Projeto '{project_root}' criado com {len(service_names)} serviço(s): {', '.join(service_names)}")


