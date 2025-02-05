#para instalar o mysql connector: pip install mysql-connector-python
#bcript para criptografar: pip install bcrypt

import mysql.connector
import os

conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="root",
    database="trabalho_bd",
)

cursor = conn.cursor()

def limpar_tela():
    os.system('clear')

def iniciar_tabelas():
    tabelas = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            remember_token VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            email_verified_at TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS categoriaPeca (
            id_categoriaPeca INT PRIMARY KEY AUTO_INCREMENT,
            codigo_categoriaPeca INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS peca (
            id_peca INT PRIMARY KEY AUTO_INCREMENT,
            codigo_peca INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL,
            preco DECIMAL(10, 2) NOT NULL,
            categoriaPeca_id INT NOT NULL,
            FOREIGN KEY (categoriaPeca_id) REFERENCES categoriaPeca(id_categoriaPeca) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INT PRIMARY KEY AUTO_INCREMENT,
            codigo_cliente INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            senha VARCHAR(50) NOT NULL,
            endereco VARCHAR(150) NOT NULL,
            telefone BIGINT NOT NULL,
            cpf VARCHAR(11) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS funcionario (
            id_funcionario INT PRIMARY KEY AUTO_INCREMENT,
            codigo_funcionario INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            endereco VARCHAR(150) NOT NULL,
            telefone BIGINT NOT NULL,
            cpf VARCHAR(11) UNIQUE NOT NULL,
            salario DECIMAL(10, 2) NOT NULL,
            cargo CHAR(1) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS build (
            id_build INT PRIMARY KEY AUTO_INCREMENT,
            codigo_build INT UNIQUE NOT NULL,
            valor DECIMAL(10, 2) NOT NULL,
            cliente_id INT NOT NULL,
            funcionario_id INT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
            FOREIGN KEY (funcionario_id) REFERENCES funcionario(id_funcionario) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS pedidoCliente (
            id_pedidoCliente INT PRIMARY KEY AUTO_INCREMENT,
            codigo_pedidoCliente INT UNIQUE NOT NULL,
            data DATE NOT NULL,
            hora TIME NOT NULL,
            cliente_id INT NOT NULL,
            funcionario_id INT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
            FOREIGN KEY (funcionario_id) REFERENCES funcionario(id_funcionario) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS itemPedido (
            id_itemPedido INT PRIMARY KEY AUTO_INCREMENT,
            codigo_itemPedido INT UNIQUE NOT NULL,
            quantidade INT NOT NULL,
            pedidoCliente_id INT NOT NULL,
            peca_id INT DEFAULT NULL,
            build_id INT DEFAULT NULL,
            FOREIGN KEY (pedidoCliente_id) REFERENCES pedidoCliente(id_pedidoCliente) ON DELETE CASCADE,
            FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE,
            FOREIGN KEY (build_id) REFERENCES build(id_build) ON DELETE CASCADE,
            CHECK (peca_id IS NOT NULL OR build_id IS NOT NULL)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS estoque (
            id_estoque INT PRIMARY KEY AUTO_INCREMENT,
            codigo_estoque INT UNIQUE NOT NULL,
            quantidade INT NOT NULL,
            peca_id INT NOT NULL,
            FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS movimentacaoEstoque (
            id_movimentacaoEstoque INT PRIMARY KEY AUTO_INCREMENT,
            codigo_movimentacaoEstoque INT UNIQUE NOT NULL,
            quantidade INT NOT NULL,
            dataMovimentacao DATETIME NOT NULL,
            peca_id INT NOT NULL,
            estoque_id INT NOT NULL,
            FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE,
            FOREIGN KEY (estoque_id) REFERENCES estoque(id_estoque) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS fornecedor (
            id_fornecedor INT PRIMARY KEY AUTO_INCREMENT,
            codigo_fornecedor INT UNIQUE NOT NULL,
            nome VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            endereco VARCHAR(150) NOT NULL,
            telefone BIGINT NOT NULL,
            cnpj VARCHAR(14) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS pagamento (
            id_pagamento INT PRIMARY KEY AUTO_INCREMENT,
            codigo_pagamento INT UNIQUE NOT NULL,
            valorPago DECIMAL(10, 2) NOT NULL,
            dataPagamento DATETIME NOT NULL,
            metodo VARCHAR(30) NOT NULL,
            status CHAR(1) NOT NULL,
            pedidoCliente_id INT NOT NULL,
            FOREIGN KEY (pedidoCliente_id) REFERENCES pedidoCliente(id_pedidoCliente) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE buildPeca(
    id_buildPeca INT PRIMARY KEY AUTO_INCREMENT,
    build_id INT NOT NULL,
    peca_id INT NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY (build_id) REFERENCES build(id_build) ON DELETE CASCADE,
    FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE
);
        """,
        """
CREATE TABLE fornecedorPeca(
    id_fornecedorPeca INT PRIMARY KEY AUTO_INCREMENT,
    fornecedor_id INT NOT NULL,
    peca_id INT NOT NULL,
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(id_fornecedor) ON DELETE CASCADE,
    FOREIGN KEY (peca_id) REFERENCES peca(id_peca) ON DELETE CASCADE
);
        """
    ]

    for tabela in tabelas:
        cursor.execute(tabela)
        cursor.nextset()
    
    conn.commit()


def listar_tabelas():
    cursor.execute("SHOW TABLES")
    for tabela in cursor:
        print(tabela)


def inserir_categoria_peca(codigo_categoriaPeca, nome):
    cursor.execute("INSERT INTO categoriaPeca (codigo_categoriaPeca, nome) VALUES (%s, %s)", (codigo_categoriaPeca, nome))
    conn.commit()
    print("Categoria de peça inserida com sucesso!")


def listar_categoria_peca():
    cursor.execute("SELECT * FROM categoriaPeca")
    for categoria in cursor:
        print(categoria)


def inserir_peca(codigo_peca, nome, preco, categoriaPeca_id):
    cursor.execute("INSERT INTO peca (codigo_peca, nome, preco, categoriaPeca_id) VALUES (%s, %s, %s, %s)", 
                   (codigo_peca, nome, preco, categoriaPeca_id))
    conn.commit()
    print("Peça inserida com sucesso!")


def listar_peca():
    cursor.execute("SELECT * FROM peca")
    for peca in cursor:
        print(peca)


def inserir_cliente(codigo_cliente, nome, email, senha, endereco, telefone, cpf):
    cursor.execute("INSERT INTO cliente (codigo_cliente, nome, email, senha, endereco, telefone, cpf) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (codigo_cliente, nome, email, senha, endereco, telefone, cpf))
    conn.commit()
    print("Cliente inserido com sucesso!")


def listar_cliente():
    cursor.execute("SELECT * FROM cliente")
    for cliente in cursor:
        print(cliente)


def inserir_funcionario(codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo):
    cursor.execute("INSERT INTO funcionario (codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                   (codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo))
    conn.commit()
    print("Funcionário inserido com sucesso!")


def listar_funcionario():
    cursor.execute("SELECT * FROM funcionario")
    for funcionario in cursor:
        print(funcionario)


def inserir_build(codigo_build, valor, cliente_id, funcionario_id):
    cursor.execute("INSERT INTO build (codigo_build, valor, cliente_id, funcionario_id) VALUES (%s, %s, %s, %s)", 
                   (codigo_build, valor, cliente_id, funcionario_id))
    conn.commit()
    print("Build inserido com sucesso!")


def listar_build():
    cursor.execute("SELECT * FROM build")
    for build in cursor:
        print(build)


def inserir_pedido_cliente(codigo_pedidoCliente, data, hora, cliente_id, funcionario_id):
    cursor.execute("INSERT INTO pedidoCliente (codigo_pedidoCliente, data, hora, cliente_id, funcionario_id) VALUES (%s, %s, %s, %s, %s)", 
                   (codigo_pedidoCliente, data, hora, cliente_id, funcionario_id))
    conn.commit()
    print("Pedido do cliente inserido com sucesso!")


def listar_pedido_cliente():
    cursor.execute("SELECT * FROM pedidoCliente")
    for pedido in cursor:
        print(pedido)


def inserir_item_pedido(codigo_itemPedido, quantidade, pedidoCliente_id, peca_id=None, build_id=None):
    cursor.execute("INSERT INTO itemPedido (codigo_itemPedido, quantidade, pedidoCliente_id, peca_id, build_id) VALUES (%s, %s, %s, %s, %s)", 
                   (codigo_itemPedido, quantidade, pedidoCliente_id, peca_id, build_id))
    conn.commit()
    print("Item do pedido inserido com sucesso!")


def listar_item_pedido():
    cursor.execute("SELECT * FROM itemPedido")
    for item in cursor:
        print(item)


def inserir_estoque(codigo_estoque, quantidade, peca_id):
    cursor.execute("INSERT INTO estoque (codigo_estoque, quantidade, peca_id) VALUES (%s, %s, %s)", 
                   (codigo_estoque, quantidade, peca_id))
    conn.commit()
    print("Estoque inserido com sucesso!")


def listar_estoque():
    cursor.execute("SELECT * FROM estoque")
    for estoque in cursor:
        print(estoque)


def inserir_movimentacao_estoque(codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id):
    cursor.execute("INSERT INTO movimentacaoEstoque (codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id) VALUES (%s, %s, %s, %s, %s)", 
                   (codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id))
    conn.commit()
    print("Movimentação de estoque inserida com sucesso!")


def listar_movimentacao_estoque():
    cursor.execute("SELECT * FROM movimentacaoEstoque")
    for movimentacao in cursor:
        print(movimentacao)


def inserir_fornecedor(codigo_fornecedor, nome, email, endereco, telefone, cnpj):
    cursor.execute("INSERT INTO fornecedor (codigo_fornecedor, nome, email, endereco, telefone, cnpj) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (codigo_fornecedor, nome, email, endereco, telefone, cnpj))
    conn.commit()
    print("Fornecedor inserido com sucesso!")


def listar_fornecedor():
    cursor.execute("SELECT * FROM fornecedor")
    for fornecedor in cursor:
        print(fornecedor)


def inserir_pagamento(codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id):
    cursor.execute("INSERT INTO pagamento (codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id))
    conn.commit()
    print("Pagamento inserido com sucesso!")


def listar_pagamento():
    cursor.execute("SELECT * FROM pagamento")
    for pagamento in cursor:
        print(pagamento)


def voltar_menu():
    input("Pressione qualquer tecla para voltar ao menu principal...")

def inserir_build_peca(build_id, peca_id, quantidade):
    cursor.execute("INSERT INTO buildPeca (build_id, peca_id, quantidade) VALUES (%s, %s, %s)", 
                   (build_id, peca_id, quantidade))
    conn.commit()
    print("BuildPeca inserido com sucesso!")

def listar_build_peca():
    cursor.execute("SELECT * FROM buildPeca")
    for buildPeca in cursor:
        print(buildPeca)

def inserir_fornecedor_peca(fornecedor_id, peca_id):
    cursor.execute("INSERT INTO fornecedorPeca (fornecedor_id, peca_id) VALUES (%s, %s)", 
                   (fornecedor_id, peca_id))
    conn.commit()
    print("FornecedorPeca inserido com sucesso!")

def listar_fornecedor_peca():
    cursor.execute("SELECT * FROM fornecedorPeca")
    for fornecedorPeca in cursor:
        print(fornecedorPeca)

# Menu principal
op = 1
while(op != '0'):
    print("Digite a opção: ")
    op = input("0 - Sair\n1 - Iniciar tabelas\n2 - Listar tabelas\n3 - Inserir categoriaPeca\n4 - Listar categoriaPeca\n5 - Inserir peca\n6 - Listar peca\n7 - Inserir cliente\n8 - Listar cliente\n9 - Inserir funcionario\n10 - Listar funcionario\n11 - Inserir build\n12 - Listar build\n13 - Inserir pedidoCliente\n14 - Listar pedidoCliente\n15 - Inserir itemPedido\n16 - Listar itemPedido\n17 - Inserir estoque\n18 - Listar estoque\n19 - Inserir movimentacaoEstoque\n20 - Listar movimentacaoEstoque\n21 - Inserir fornecedor\n22 - Listar fornecedor\n23 - Inserir pagamento\n24 - Listar pagamento\n25 - Inserir buildPeca\n26 - Listar buildPeca\n27 - Inserir fornecedorPeca\n28 - Listar fornecedorPeca\n")

    if op == '1':
        iniciar_tabelas()
    elif op == '2':
        listar_tabelas()
    elif op == '3':
        codigo_categoriaPeca = input("Digite o código da categoria da peça: ")
        nome = input("Digite o nome da categoria da peça: ")
        inserir_categoria_peca(codigo_categoriaPeca, nome)
    elif op == '4':
        listar_categoria_peca()
    elif op == '5':
        codigo_peca = input("Digite o código da peça: ")
        nome = input("Digite o nome da peça: ")
        preco = input("Digite o preço da peça: ")
        categoriaPeca_id = input("Digite o id da categoria da peça: ")
        inserir_peca(codigo_peca, nome, preco, categoriaPeca_id)
    elif op == '6':
        listar_peca()
    elif op == '7':
        codigo_cliente = input("Digite o código do cliente: ")
        nome = input("Digite o nome do cliente: ")
        email = input("Digite o email do cliente: ")
        senha = input("Digite a senha do cliente: ")
        endereco = input("Digite o endereço do cliente: ")
        telefone = input("Digite o telefone do cliente: ")
        cpf = input("Digite o CPF do cliente: ")
        inserir_cliente(codigo_cliente, nome, email, senha, endereco, telefone, cpf)
    elif op == '8':
        listar_cliente()
    elif op == '9':
        codigo_funcionario = input("Digite o código do funcionário: ")
        nome = input("Digite o nome do funcionário: ")
        email = input("Digite o email do funcionário: ")
        endereco = input("Digite o endereço do funcionário: ")
        telefone = input("Digite o telefone do funcionário: ")
        cpf = input("Digite o CPF do funcionário: ")
        salario = input("Digite o salário do funcionário: ")
        cargo = input("Digite o cargo do funcionário (ex: 'A' para administrador): ")
        inserir_funcionario(codigo_funcionario, nome, email, endereco, telefone, cpf, salario, cargo)
    elif op == '10':
        listar_funcionario()
    elif op == '11':
        codigo_build = input("Digite o código do build: ")
        valor = input("Digite o valor do build: ")
        cliente_id = input("Digite o id do cliente: ")
        funcionario_id = input("Digite o id do funcionário: ")
        inserir_build(codigo_build, valor, cliente_id, funcionario_id)
    elif op == '12':
        listar_build()
    elif op == '13':
        codigo_pedidoCliente = input("Digite o código do pedido do cliente: ")
        data = input("Digite a data do pedido (formato: yyyy-mm-dd): ")
        hora = input("Digite a hora do pedido (formato: hh:mm:ss): ")
        cliente_id = input("Digite o id do cliente: ")
        funcionario_id = input("Digite o id do funcionário: ")
        inserir_pedido_cliente(codigo_pedidoCliente, data, hora, cliente_id, funcionario_id)
    elif op == '14':
        listar_pedido_cliente()
    elif op == '15':
        codigo_itemPedido = input("Digite o código do item do pedido: ")
        quantidade = input("Digite a quantidade do item: ")
        pedidoCliente_id = input("Digite o id do pedido do cliente: ")
        peca_id = input("Digite o id da peça (ou pressione Enter para não informar): ")
        build_id = input("Digite o id do build (ou pressione Enter para não informar): ")
        inserir_item_pedido(codigo_itemPedido, quantidade, pedidoCliente_id, peca_id or None, build_id or None)
    elif op == '16':
        listar_item_pedido()
    elif op == '17':
        codigo_estoque = input("Digite o código do estoque: ")
        quantidade = input("Digite a quantidade do estoque: ")
        peca_id = input("Digite o id da peça: ")
        inserir_estoque(codigo_estoque, quantidade, peca_id)
    elif op == '18':
        listar_estoque()
    elif op == '19':
        codigo_movimentacaoEstoque = input("Digite o código da movimentação de estoque: ")
        quantidade = input("Digite a quantidade movimentada: ")
        dataMovimentacao = input("Digite a data e hora da movimentação (formato: yyyy-mm-dd hh:mm:ss): ")
        peca_id = input("Digite o id da peça: ")
        estoque_id = input("Digite o id do estoque: ")
        inserir_movimentacao_estoque(codigo_movimentacaoEstoque, quantidade, dataMovimentacao, peca_id, estoque_id)
    elif op == '20':
        listar_movimentacao_estoque()
    elif op == '21':
        codigo_fornecedor = input("Digite o código do fornecedor: ")
        nome = input("Digite o nome do fornecedor: ")
        email = input("Digite o email do fornecedor: ")
        endereco = input("Digite o endereço do fornecedor: ")
        telefone = input("Digite o telefone do fornecedor: ")
        cnpj = input("Digite o CNPJ do fornecedor: ")
        inserir_fornecedor(codigo_fornecedor, nome, email, endereco, telefone, cnpj)
    elif op == '22':
        listar_fornecedor()
    elif op == '23':
        codigo_pagamento = input("Digite o código do pagamento: ")
        valorPago = input("Digite o valor pago: ")
        dataPagamento = input("Digite a data do pagamento (formato: yyyy-mm-dd hh:mm:ss): ")
        metodo = input("Digite o método de pagamento: ")
        status = input("Digite o status do pagamento (P para pago, A para aguardando): ")
        pedidoCliente_id = input("Digite o id do pedido do cliente: ")
        inserir_pagamento(codigo_pagamento, valorPago, dataPagamento, metodo, status, pedidoCliente_id)
    elif op == '24':
        listar_pagamento()
    elif op == '25':
        build_id = input("Digite o código do build: ")
        peca_id = input("Digite o código da peça: ")
        quantidade = input("Digite a quantidade: ")
        inserir_build_peca(build_id, peca_id, quantidade)
    elif op == '26':
        listar_build_peca()
    elif op == '27':
        fornecedor_id = input("Digite o código do fornecedor: ")
        peca_id = input("Digite o código da peça: ")
        inserir_fornecedor_peca(fornecedor_id, peca_id)
    elif op == '28':
        listar_fornecedor_peca()

    limpar_tela()
