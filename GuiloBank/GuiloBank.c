// Bibliotecas usadas no projeto
#include <ctype.h>
#include <Locale.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

// Const char para nao precisar ficar escrevendo o nome do arquivo todas as vezes
const char *ARQUIVO_SALDO_POUPANCA = "saldo_poupanca.txt";
const char *ARQUIVO_SEGURANCA = "senha.txt";
const char *ARQUIVO_SALDO_CONTA = "saldo_conta.txt";
const char *ARQUIVO_RECEITA_GASTO = "receita_gasto.txt";
const char *ARQUIVO_INVESTIMENTO = "investimento.txt";
const char *ARQUIVO_EMPRESTIMO = "emprestimo.txt";

// Struct para fazer o cadastro de receitas e gastos
struct ecadastro {
  char descricao[240];
  char categoria[240];
  char valor[10];
  int dia, mes, ano;
};

// Funcao para calcular os juros da poupanca
double juros_compostos(const float saldos, const int mes) {
  return saldos * pow(1.01, mes);
}

// Funcao para criar o arquivo *.txt se nao exista
void cria_arquivo_se_nao_existe(const char *nome_arquivo) {
  FILE *file = fopen(nome_arquivo, "r");
  if (file) {
    fclose(file);
  } else {
    FILE *file = fopen(nome_arquivo, "a");
    fclose(file);
  }
}

// Funcao para confirmar se a senha do usuario e a correta
int confirma_senha() {
  FILE *seguranca = fopen(ARQUIVO_SEGURANCA, "r+");
  char senha_confirmacao[255];
  printf("Confirme sua senha: ");
  scanf("%s", senha_confirmacao);
  char senha_arquivo[255];
  fscanf(seguranca, "%s", senha_arquivo);
  while (strcmp(senha_confirmacao, senha_arquivo) != 0) {
    printf("\nSenha incorreta!\n");
    printf("Confirme sua senha: ");
    scanf("%s", senha_confirmacao);
  }
  printf("Senha confirmada!\n\n");
  return 0;
  fclose(seguranca);
}

// Funcao para ver se um arquivo ja existe
int arquivo_existe(const char *nome_arquivo) {
  FILE *emprestimo = fopen(nome_arquivo, "r");

  if (emprestimo == NULL)
    return 0;

  if (feof(emprestimo)) {
    fclose(emprestimo);
    return 0;
  }

  fclose(emprestimo);
  return 1;
}

// Funcao para o usuario criar a sua senha ou entrar no menu, caso ja tenha
// criado a sua senha
void entrar_conta() {
  cria_arquivo_se_nao_existe(ARQUIVO_SEGURANCA);

  while (1) {
    printf("\n-------------------------\n");
    printf("\033[92mBem vindo ao GUILO BANK!\033[0m \n\n");
    printf("E a sua primeira vez acessando o nosso banco?\n\n"
           " 0 - Sim, primeira vez!\n"
           " 1 - Nao, ja possuo conta GUILO BANK!\n\n");

    int possui_conta;
    scanf("%d", &possui_conta);

    if (possui_conta == 1) {
      printf("Por favor, digite sua senha.\n");
      char senha[255], senha_salva[255];
      scanf("%s", senha);
      FILE *seguranca = fopen(ARQUIVO_SEGURANCA, "r+");
      fscanf(seguranca, "%s", senha_salva);
      if (strcmp(senha_salva, senha) == 0) {
        break;
      } else {
        printf("Senha incorreta!");
      }
    } else if (possui_conta == 0) {
      fclose(fopen(ARQUIVO_SEGURANCA, "w"));
      FILE *seguranca = fopen(ARQUIVO_SEGURANCA, "r+");
      printf("Muito obrigado por nos escolher!\n"
             "Crie uma senha para a sua nova conta GUILO BANK!\n\n");
      char senha_nova[255];
      scanf("%s", senha_nova);
      fprintf(seguranca, "%s", senha_nova);
      fclose(seguranca);
      FILE *seguranca_confimar = fopen(ARQUIVO_SEGURANCA, "r+");
      printf("Confirme sua senha.\n");
      char senha_confirmacao[255];
      scanf("%s", senha_confirmacao);
      while (strcmp(senha_confirmacao, senha_nova) != 0) {
        printf("\nSenha incorreta!\n");
        printf("Confirme sua senha.\n");
        scanf("%s", senha_confirmacao);
      }
      printf("Senha confirmada!\n");
      return;
      fclose(seguranca_confimar);
    } else {
      printf("\033[92mDigite uma opcao valida!\033[0m\n");
      printf("-------------------------\n");
    }
  }
}

// Funcao criada para armazenar a receita ou gasto do usuario
// A funcao tambem cria arquivos de meses e anos específicos para a geracao dos relatorios
//Tivemos dificuldade em criar os arquivos específicos com as variaveis necessarias
void le_cadastro(const char *receita_ou_gasto) {
  struct ecadastro c = {};
  FILE *arquivo;
  char arquivo_nome[50];

  printf("Qual o valor do produto? \n");
  printf("R$: ");
  scanf("%s", c.valor);
  printf("Qual dia? \n");
  scanf("%d", &c.dia);
  while (c.dia < 1 || c.dia > 31) {
    printf("Insira um dia valido!\n");
    printf("Qual dia? \n");
    scanf("%d", &c.dia);
  }
  printf("Qual mes? \n");
  scanf("%d", &c.mes);
  while (c.mes < 1 || c.mes > 12) {
    printf("Insira um mes valido!\n");
    printf("Qual mes? \n");
    scanf("%d", &c.mes);
  }
  printf("Qual ano?\n");
  scanf("%d", &c.ano);
  printf("Faca uma breve descricao do produto. Use '_' para separar cada "
         "palavra.\n");
  scanf("%s", c.descricao);
  printf("De qual categoria? (Ex: Moradia/Transporte/Alimentacao) Use '_' para "
         "separar cada palavra.\n");
  scanf("%s", c.categoria);
  printf("\n");
  printf("\n-------------------------\n");

  sprintf(arquivo_nome, "%s_%04d_%02d", c.categoria, c.ano, c.mes);
  arquivo = fopen(arquivo_nome, "ab");
  if (arquivo == NULL) {
    printf("Dados nao encontrados.\n");
    return;
  } else {
    fwrite(&c, sizeof(struct ecadastro), 1, arquivo);
  }
  fclose(arquivo);

  FILE *arquivo_txt;
  char arquivo_nome_txt[50];

  sprintf(arquivo_nome_txt, "%s_%04d_%02d.txt", c.categoria, c.ano, c.mes);
  arquivo_txt = fopen(arquivo_nome_txt, "a");
  if (arquivo_txt == NULL) {
    printf("Dados nao encontrados.\n");
    return;
  } else {
    fprintf(arquivo_txt, "Categoria: %s\n", c.categoria);
    fprintf(arquivo_txt, "Descricao: %s\n", c.descricao);
    fprintf(arquivo_txt, "Valor: %s\n", c.valor);
    fprintf(arquivo_txt, "Data: %02d/%02d/%04d\n", c.dia, c.mes, c.ano);
  }

  fclose(arquivo_txt);

  FILE *arquivo_secundario;

  sprintf(arquivo_nome, "receita_gasto_%04d", c.ano);
  arquivo_secundario = fopen(arquivo_nome, "ab");
  if (arquivo_secundario == NULL) {
    printf("Erro ao abrir o arquivo.\n");
    return;
  } else {
    fwrite(&c, sizeof(struct ecadastro), 1, arquivo_secundario);
  }
  fclose(arquivo_secundario);

  FILE *arquivo_txt_secundario;

  sprintf(arquivo_nome_txt, "receita_gasto_%04d.txt", c.ano);
  arquivo_txt_secundario = fopen(arquivo_nome_txt, "a");
  if (arquivo_txt_secundario == NULL) {
    printf("Erro ao abrir o arquivo.\n");
    return;
  } else {
    fprintf(arquivo_txt_secundario, "Categoria: %s\n", c.categoria);
    fprintf(arquivo_txt_secundario, "Descricao: %s\n", c.descricao);
    fprintf(arquivo_txt_secundario, "Valor: %s\n", c.valor);
    fprintf(arquivo_txt_secundario, "Data: %02d/%02d/%04d\n", c.dia, c.mes,
            c.ano);
  }

  fclose(arquivo_txt_secundario);

  FILE *ARQUIVO_BINARIO_RECEITA_GASTO =
      fopen("receita_gasto_binario.txt", "ab");

  fwrite(&c, sizeof(struct ecadastro), 1, ARQUIVO_BINARIO_RECEITA_GASTO);

  fclose(ARQUIVO_BINARIO_RECEITA_GASTO);

  FILE *arquivo_receita_gasto = fopen(ARQUIVO_RECEITA_GASTO, "a");
  fprintf(arquivo_receita_gasto, "\n-------------------------\n");
  fprintf(arquivo_receita_gasto, "%s\n", receita_ou_gasto);
  fprintf(arquivo_receita_gasto, "Valor: R$ %s\n", c.valor);
  fprintf(arquivo_receita_gasto, "Dia: %d\n", c.dia);
  fprintf(arquivo_receita_gasto, "Mes: %d\n", c.mes);
  fprintf(arquivo_receita_gasto, "Ano: %d\n", c.ano);
  fprintf(arquivo_receita_gasto, "Descricao: %s\n", c.descricao);
  fprintf(arquivo_receita_gasto, "Categoria: %s\n", c.categoria);

  fclose(arquivo_receita_gasto);
}

// Funcao para orientar o usuario nos quesitos de receita e gastos
void receita_gasto() {
  while (1) {
    printf("\033[92mCadastro de receitas e gastos\033[0m\n");
    printf("-------------------------\n");
    printf("\n"
           " 1- Declarar receita \n"
           " 2- Declarar gasto\n\n"
           " 0- Voltar ao menu\n\n");
    int option;
    scanf("%d", &option);

    if (option == 1) {
      printf("\n\033[92mReceitas\033[0m \n");
      le_cadastro("Receita");
    }

    else if (option == 2) {
      printf("\n\033[92mGastos\033[0m\n");
      le_cadastro("Gasto");
    } else if (option == 0) {
      break;
    } else {
      printf("\033[92mDigite uma opcao valida!\033[0m\n");
      printf("-------------------------\n");
    }
  }
}

//Funcao para pegar o arquivo do mes específico e mostrar ao usuario
//Tivemos dificuldade para poder pegar a variavel mes e comparar com o arquivo
void relatorio_mes() {
  struct ecadastro c;
  FILE *arquivo;
  char arquivo_nome[50];
  printf("Digite a categoria que deseja: \n");
  scanf("%s", c.categoria);
  printf("Digite o mes que deseja ver no relatorio: \n");
  scanf("%d", &c.mes);
  printf("Digite o ano que deseja ver no relatorio: \n");
  scanf("%d", &c.ano);

  if (c.mes == 1) {
    c.mes = 12;
    c.ano = c.ano - 1;
    sprintf(arquivo_nome, "%s_%04d_%02d", c.categoria, c.ano, c.mes);
    arquivo = fopen(arquivo_nome, "rb");
    if (arquivo == NULL) {
      printf("\nNao ha registros para essa categoria/mes/ano\n");
      return;
    } else {
      while (fread(&c, sizeof(struct ecadastro), 1, arquivo) != 0) {
        printf("Categoria: %s\n", c.categoria);
        printf("Descricao: %s\n", c.descricao);
        printf("Valor: %s\n", c.valor);
        printf("Data: %02d/%02d/%04d\n", c.dia, c.mes, c.ano);
      }
    }
    fclose(arquivo);
  } else {
    sprintf(arquivo_nome, "%s_%04d_%02d", c.categoria, c.ano, c.mes);
    arquivo = fopen(arquivo_nome, "rb");
    if (arquivo == NULL) {
      printf("\nNao ha registros para essa categoria/mes/ano\n");
      return;
    } else {
      while (fread(&c, sizeof(struct ecadastro), 1, arquivo) != 0) {
        printf("\n\n-------------------------\n");
        printf("Categoria: %s\n", c.categoria);
        printf("Descricao: %s\n", c.descricao);
        printf("Valor: %s\n", c.valor);
        printf("Data: %02d/%02d/%04d\n", c.dia, c.mes, c.ano);
        printf("-------------------------\n");
      }
    }
    fclose(arquivo);
  }
}

//Funcao para pegar o arquivo do ano específico e mostrar ao usuario
//Tivemos dificuldade para poder pegar a variavel mes e comparar com o arquivo
void relatorio_ano() {
  struct ecadastro c;
  FILE *arquivo_secundario;
  char arquivo_nome[50];
  printf("\nQual o ano que deseja ver o relatorio? \n");
  scanf("%d", &c.ano);

  sprintf(arquivo_nome, "receita_gasto_%04d", c.ano);
  arquivo_secundario = fopen(arquivo_nome, "rb");
  if (arquivo_secundario == NULL) {
    printf("\nNao ha registros para essa categoria/mes/ano\n");
    return;
  } else {
    
    while (fread(&c, sizeof(struct ecadastro), 1, arquivo_secundario) != 0) {
      printf("\n\n-------------------------\n");
      printf("Categoria: %s\n", c.categoria);
      printf("Descricao: %s\n", c.descricao);
      printf("Valor: R$%s\n", c.valor);
      printf("Data: %02d/%02d/%04d\n", c.dia, c.mes, c.ano);
      printf("-------------------------\n");
    }
  }
  fclose(arquivo_secundario);
}
// Funcao para ver se e possível mostrar o relatorio para o usuario
void rel_transacao() {
  struct ecadastro c;
  while (1) {
    printf("\033[92mRelatorio de transacao\033[0m\n");
    printf("-------------------------\n");
    printf("\n"
           " 1- Relatorio de transacao dos ultimos 12 meses\n"
           " 2- Relatorio de transacao do ultimo mes\n\n"
           " 0- Voltar ao menu\n\n");
    int option;
    scanf("%d", &option);
    if (option == 1) {
      printf("\n\033[92mRelatorio dos ultimos 12 mes\033[0m\n\n");
      relatorio_ano();
      return;
    } else if (option == 2) {
      printf("\n\033[92mRelatorio do ultimo mes\033[0m\n\n");
      relatorio_mes();
      return;
    } else if (option == 0) {
      break;
    } else {
      printf("\n\033[92mDigite uma opcao valida!\033[0m\n");
      printf("-------------------------\n");
    }
  }
}

// Funcao para o usuario fazer uma transferencia para outro usuario
void transferencia() {
  float saldo_conta = 0;
  char nome[25], numero_agencia[7], conta_agencia[7];
  float valor_transferencia = 0;
  cria_arquivo_se_nao_existe(ARQUIVO_SALDO_CONTA);
  FILE *arquivo_saldo_conta = fopen(ARQUIVO_SALDO_CONTA, "r+");
  fscanf(arquivo_saldo_conta, "%f", &saldo_conta);
  printf("\033[92mTransferencia\033[0m\n");
  printf("-------------------------\n");

  printf("Voce deseja fazer uma transferencia?\n"
         "0 - Nao\n"
         "1 - Sim\n\n");
  int option;
  scanf("%d", &option);
  if (option == 0) {
    return;
  } else if (option == 1)
    printf("Nome do titular da conta\n");
  printf("Nome: ");
  scanf("%s", nome);
  printf("Agencia (Somente numeros): ");
  scanf("%s", numero_agencia);
  printf("Conta (Somente numeros): ");
  scanf("%s", conta_agencia);
  printf("Quanto voce quer transferir para %s? R$", nome);
  scanf("%f", &valor_transferencia);
  confirma_senha();
  if (saldo_conta < valor_transferencia) {
    printf("Saldo insuficiente. Voce tem %.2f na sua conta!\n\n", saldo_conta);
  } else {
    saldo_conta -= valor_transferencia;
    fseek(arquivo_saldo_conta, 0, SEEK_SET);
    fprintf(arquivo_saldo_conta, "%.2f", saldo_conta);
    printf("Transferido R$%.2f para %s!\n", valor_transferencia, nome);
    printf("Seu novo saldo da conta corrente e de R$%.2f!\n\n", saldo_conta);
  }
  fclose(arquivo_saldo_conta);
}

// Funcao para o usuario retirar e colocar dinheiro na poupanca
// Se tiver dinheiro na poupanca, o usuario podera ver o rendimento futuro do
// seu saldo
void poupanca() {

  cria_arquivo_se_nao_existe(ARQUIVO_SALDO_POUPANCA);
  cria_arquivo_se_nao_existe(ARQUIVO_SALDO_CONTA);
  while (1) {
    float saldo_poupanca = 0;
    float saldo_conta = 0;
    FILE *arquivo_saldo_poupanca = fopen(ARQUIVO_SALDO_POUPANCA, "r+");
    fscanf(arquivo_saldo_poupanca, "%f", &saldo_poupanca);
    FILE *arquivo_saldo_conta = fopen(ARQUIVO_SALDO_CONTA, "r+");
    fscanf(arquivo_saldo_conta, "%f", &saldo_conta);
    printf("\033[92mPoupanca\033[0m\n");
    printf("-------------------------\n");
    printf("\n"
           " 1- Ver Saldo\n"
           " 2- Depositar\n"
           " 3- Sacar dinheiro\n"
           " 4- Ver rendimento\n\n"
           " 0- Voltar ao menu\n\n");
    int option;
    scanf("%d", &option);

    if (option == 1) {
      printf("Voce possui R$%.2f no total.\n\n", saldo_poupanca);
      printf("-------------------------\n");
    } else if (option == 2) {
      float valor;
      printf("Deseja depositar quanto?\n");
      scanf("%f", &valor);
      if (saldo_conta < valor) {
        printf("Saldo na conta corrente inferior ao valor de deposito!\n");
      } else {
        printf("\nVoce depositou R$%.2f!\n", valor);
        saldo_poupanca += valor;
        saldo_conta -= valor;
        fseek(arquivo_saldo_poupanca, 0, SEEK_SET);
        fprintf(arquivo_saldo_poupanca, "%.2f", saldo_poupanca);
        fseek(arquivo_saldo_conta, 0, SEEK_SET);
        fprintf(arquivo_saldo_conta, "%.2f", saldo_conta);
        printf("Seu novo saldo e de R$%.2f!\n\n", saldo_poupanca);
        printf("-------------------------\n");
      }
    } else if (option == 3) {

      float valor;
      printf("Qual quantia voce quer retirar?\n");
      scanf("%f", &valor);
      if (saldo_poupanca < valor) {
        printf("\nSaldo insuficiente. Voce tem %.2f na sua poupanca!\n\n",
               saldo_poupanca);
      } else {
        confirma_senha();
        saldo_poupanca -= valor;
        fseek(arquivo_saldo_poupanca, 0, SEEK_SET);
        fprintf(arquivo_saldo_poupanca, "%.2f", saldo_poupanca);
        printf("\nRetirado %.2f \nAgora voce tem %.2f na sua poupanca!\n\n",
               valor, saldo_poupanca);
        saldo_conta += valor;
        fseek(arquivo_saldo_conta, 0, SEEK_SET);
        fprintf(arquivo_saldo_conta, "%.2f", saldo_conta);
        printf("-------------------------\n");
      }

    } else if (option == 4) {
      printf("\033[92mRendimento\033[0m\n\n");
      if (saldo_poupanca == 0) {
        printf("Deposite um valor para seu dinheiro render!\n");
      } else {
        printf("Essa e a poupanca Guilo bank! O rendimento das contas do banco "
               "e 1%% ao mes!\n\n");

        printf("Voce deseja ver seu rendimento na sua poupanca daqui a quantos "
               "meses? ");
        int mes;
        scanf("%d", &mes);
        if (mes <= 0) {
          printf("Digite um mes valido!\n");
        } else {
          printf(
              "\nCom este saldo atual daqui a %d mes(es) vc tera R$%.2f!\n\n",
              mes, juros_compostos(saldo_poupanca, mes));
          printf("-------------------------\n");
        }
      }
    } else if (option == 0) {
      return;
    } else {
      printf("\033[92mDigite uma opcao valida!\033[0m\n");
      printf("-------------------------\n");
    }
    fclose(arquivo_saldo_poupanca);
    fclose(arquivo_saldo_conta);
  }
}

// Funcao para criar uma conta corrente ao usuario
void conta_corrente() {

  cria_arquivo_se_nao_existe(ARQUIVO_SALDO_CONTA);
  FILE *arquivo_saldo_conta = fopen(ARQUIVO_SALDO_CONTA, "r+");
  float saldo_conta = 0;
  while (1) {
    fscanf(arquivo_saldo_conta, "%f", &saldo_conta);

    printf("\033[92mConta Corrente\033[0m\n");
    printf("-------------------------\n");
    printf("\n"
           " 1- Ver Saldo\n"
           " 2- Depositar\n"
           " 3- Sacar dinheiro\n\n"
           " 0- Voltar ao menu\n\n");
    int option;
    scanf("%d", &option);

    if (option == 1) {
      printf("Voce possui R$:%.2f no total.\n\n", saldo_conta);
    } else if (option == 2) {
      float valor;
      printf("Qual e o valor do deposito?\n");
      scanf("%f", &valor);
      confirma_senha();
      printf("Voce depositou R$%.2f!\n", valor);
      saldo_conta += valor;
      fseek(arquivo_saldo_conta, 0, SEEK_SET);
      fprintf(arquivo_saldo_conta, "%.2f", saldo_conta);
      printf("Seu novo saldo e de R$%.2f!\n\n", saldo_conta);
    } else if (option == 3) {
      printf("Qual quantia voce quer retirar?\n");
      float valor;
      scanf("%f", &valor);
      confirma_senha();
      if (saldo_conta < valor) {
        printf("Saldo insuficiente. Voce tem R$%.2f na sua conta!\n\n",
               saldo_conta);
      } else {
        saldo_conta -= valor;
        fseek(arquivo_saldo_conta, 0, SEEK_SET);
        fprintf(arquivo_saldo_conta, "%.2f", saldo_conta);
        printf("Retirado R$%.2f \nAgora voce tem R$%.2f na sua conta.\n\n",
               valor, saldo_conta);
        printf("-------------------------\n");
      }

    } else if (option == 0) {
      break;
    } else {
      printf("\033[92mDigite uma opcao valida!\033[0m\n");
      printf("-------------------------\n");
    }
  }
  fclose(arquivo_saldo_conta);
}

// Funcao para o usuario comprar uma acao de investimento
void comprar_acao(const char *nome_empresa, const float valor_acao, float saldo_conta) {
  FILE *investimento = fopen(ARQUIVO_INVESTIMENTO, "a");
  FILE *saldo_conta_corrente = fopen(ARQUIVO_SALDO_CONTA, "r+");
  printf("Voce tem R$%.2f esperando para investir \n", saldo_conta);
  printf("Quantas acoes voce quer comprar?\n");
  int acao;
  scanf("%d", &acao);
  float preco_compra = acao * valor_acao;
  printf("Voce comprara R$%.2f em acao(oes)!\n", preco_compra);
  confirma_senha();
  if (preco_compra < saldo_conta) {
    printf("Voce comprou %d acao(oes)!\n", acao);
    saldo_conta -= preco_compra;
    fprintf(saldo_conta_corrente, "%.2f\n", saldo_conta);
    fseek(saldo_conta_corrente, 0, SEEK_SET);
    printf("Agora voce tem R$%.2f disponível na sua conta corrente.\n",
           saldo_conta);
    fprintf(investimento, "-------------------------\n");
    fprintf(investimento, "%s\n", nome_empresa);
    fprintf(investimento, "Quantidade: %d\n", acao);
    fprintf(investimento, "Valor de cada acao: R$%.2f\n", valor_acao);
    fprintf(investimento, "Dinheiro investido: R$%.2f\n", preco_compra);
    fclose(investimento);
  } else {
    printf("Saldo indisponivel!\n");
    printf("Voce tem R$%.2f disponível para investir.\n", saldo_conta);
    return;
  }
  return;
}

// Funcao para o usuario ver as empresas disponíveis para investimento,
// mostrando nome da empresa e preco da acao.
void investimento() {
  float valor_petro = 1 + (rand() % 27);
  float valor_tesla = 1 + (rand() % 63);
  float valor_fei = 1 + (rand() % 31);
  cria_arquivo_se_nao_existe(ARQUIVO_INVESTIMENTO);
  FILE *saldo_conta_corrente = fopen(ARQUIVO_SALDO_CONTA, "r+");
  FILE *investimento = fopen(ARQUIVO_INVESTIMENTO, "r+");
  while (1) {
    printf("\033[92mInvestimento\033[0m\n");
    printf("-------------------------\n");
    printf("\n"
           " 1 - Ver empresas para investir\n"
           " 2 - Ver investimentos\n"
           " 3 - Retirar dinheiro\n\n"
           " 0 - Voltar ao menu\n\n");
    int option;
    scanf("%d", &option);
    if (option == 0) {
      return;

    } else if (option == 1) {
      printf("\n1- PETROBRAS - PETR4\n"
             "Valor de cada acao: R$%.2f\n\n",
             valor_petro);
      printf("2-  TESLA - TSLA34\n"
             "Valor de cada acao: R$%.2f\n\n",
             valor_tesla);
      printf("3- FEI INVEST - FEII4\n"
             "Valor de cada acao: R$%.2f\n\n",
             valor_fei);
      int empresa;
      printf("Qual empresa voce quer investir?\n");
      scanf("%d", &empresa);
      float saldo_conta;
      fscanf(saldo_conta_corrente, "%f", &saldo_conta);
      if (empresa == 1) {
        comprar_acao("Petrobras", valor_petro, saldo_conta);
        return;

      } else if (empresa == 2) {
        comprar_acao("Tesla", valor_tesla, saldo_conta);
        return;

      } else if (empresa == 3) {
        comprar_acao("FEI INVEST", valor_fei, saldo_conta);
        return;

      } else {
        printf("Digite uma opcao valida\n");
        return;
      }
      fclose(investimento);
    } else if (option == 2) {
      FILE *investimento = fopen(ARQUIVO_INVESTIMENTO, "r");
      char linha[100];
      char *result;
      int i;
      while (!feof(investimento)) {
        result = fgets(linha, 100, investimento);
        if (result)
          printf("%s", linha);
        i++;
      }
      return;
    } else if (option == 3) {

      return;
    }
    fclose(investimento);
  }
}

// Funcao para o usuario criar um cartao para compras online mais seguras
void cartao_online() {

  printf("\033[92mCartao Online\033[0m \n");
  printf("-------------------------\n");
  while (1) {
    printf("Utilize do cartao para comprar comprar onlines e nao se preocupe "
           "com golpes! \n");
    confirma_senha();
    printf("\nEspere um instante, estamos gerando seu cartao online!");
    int numero_1 = 1000 + (rand() % 8999);
    int numero_2 = 1000 + (rand() % 8999);
    int numero_3 = 1000 + (rand() % 8999);
    int numero_4 = 1000 + (rand() % 8999);
    int cvv = 100 + (rand() % 900);
    int mes = 1 + (rand() % 12);
    int ano = 23 + (rand() % 4);

    printf("\n");
    sleep(4);
    printf("\n-------------------------------------------\n");
    printf(" | Numero do cartao: %d-%d-%d-%d \n", numero_1, numero_2, numero_3,
           numero_4);
    printf(" | CVV: %d \n", cvv);
    printf(" | Validade: %d/%d \n", mes, ano);
    printf("-------------------------------------------\n");
    break;
  }
}

// Funcao para o usuario pedir um emprestimo ao nosso banco
void emprestimo_bancario() {

  printf("\033[92mEmprestimo Bancario\033[0m\n");
  printf("-------------------------\n");
  printf("\n"
         " 1- Ver emprestimo\n"
         " 2- Fazer emprestimo\n\n"

         " 0- Voltar ao menu\n\n");
  int option;
  scanf("%d", &option);
  if (option == 1) {
    if (!arquivo_existe(ARQUIVO_EMPRESTIMO)) {
      printf("Voce ainda nao realizou nenhum emprestimo.\n");
    } else {
      FILE *emprestimo = fopen(ARQUIVO_EMPRESTIMO, "r");
      char linha[100];
      char *result;
      int i;
      while (!feof(emprestimo)) {
        result = fgets(linha, 100, emprestimo);
        if (result)
          printf("%s", linha);
        i++;
      }
    }
  } else if (option == 2) {
    if (arquivo_existe(ARQUIVO_EMPRESTIMO)) {
      printf("\nVoce ja fez um emprestimo, so e possivel um por vez!\n");
    } else {
      while (1) {
        cria_arquivo_se_nao_existe(ARQUIVO_EMPRESTIMO);
        FILE *emprestimo = fopen(ARQUIVO_EMPRESTIMO, "w");
        printf("Precisando de um emprestimo para realizar seu sonho?\n");
        confirma_senha();
        printf("\nVamos comecar o processo para pegar seu emprestimo!\n\n");
        printf(
            "Antes de tudo saiba que o GUILO BANK, ao final de 1 ano de "
            "emprestimo, cobra 5%% de juros em relacao a quantidade creditada "
            "e aceita apenas valores maiores de R$10.000.\n\n");
        printf("Por favor, insira seus dados pessoais.\n");
        char nome_completo[255];
        char cpf[255];
        char telefone[255];
        float valor = 0;
        printf("Nome completo: ");
        scanf("%s", nome_completo);
        printf("CPF: ");
        scanf("%s", cpf);
        printf("Numero de Telefone: ");
        scanf("%s", telefone);
        printf("Quantia para receber: R$");
        scanf("%f", &valor);
        while (valor < 10000) {
          printf("\nValor de emprestimo menor que permitdo(R$10.000)\n");
          printf("Quantia para receber: R$");
          scanf("%f", &valor);
        }
        printf("\nAo passar por essa etapa, voce esta concordando com os "
               "termos de "
               "emprestimos e esta de acordo com a quantida de R$%.2f "
               "creditada.\n",
               valor);
        float valor_do_juros = valor * 0.05;
        valor += valor_do_juros;
        printf(
            "Com esse valor, daqui ha 1 ano, voce tera uma cobranca de R$%.2f "
            "(valor do emprestimo com 5%% de juros!)\n",
            valor);
        printf("Tem certeza que deseja continuar?\n\n"
               "0- SIM, ESTOU DE ACORDO\n"
               "1- NaO, QUERO REVER O ACORDO/QUANTIA\n\n");
        int option;
        scanf("%d", &option);
        if (option == 0) {
          printf("\nValor de emprestimo creditado (R$%.2f)!\n"
                 "Realize seu sonho!\n",
                 valor);
          fprintf(emprestimo, "-------------------------\n");
          fprintf(emprestimo, "Nome completo: %s\n", nome_completo);
          fprintf(emprestimo, "CPF: %s\n", cpf);
          fprintf(emprestimo, "Numero telefone: %s\n", telefone);
          fprintf(emprestimo, "Dinheiro do emprestimo: R$%.2f\n", valor);
          fclose(emprestimo);
          return;
        } else if (option == 1) {
          printf("Ok, sem problemas!\n\n");
        } else {
          printf("Digite uma opcao correta!");
        }
      }
    }
  } else {
    printf("Opcao Invalida");
  }
}

// Funcao para armazenar genericamente o nome do produto e o seu valor
void produtos_loja(const char *unidade, const char *nome_produto,
                   const float valor_unitario) {
  FILE *saldo_conta_corrente = fopen(ARQUIVO_SALDO_CONTA, "r+");
  printf("Voce deseja quantos %s de %s?\n", unidade, nome_produto);
  int qtd_produto;
  scanf("%d", &qtd_produto);
  float valor_total = qtd_produto * valor_unitario;
  printf("O valor total da sua compra e: R$%.2f\n", valor_total);
  confirma_senha();
  printf("Parabens! Voce comprou %d %s de %s\n", qtd_produto, unidade,
         nome_produto);
  float saldo_conta = 0;
  fscanf(saldo_conta_corrente, "%f", &saldo_conta);

  if (saldo_conta < valor_total) {
    printf("O valor da compra e maior que o saldo da sua conta corrente\n");
  } else {
    saldo_conta -= valor_total;
    printf("Seu novo saldo na conta corrente e R$%.2f\n\n", saldo_conta);
  }
  fseek(saldo_conta_corrente, 0, SEEK_SET);
  fprintf(saldo_conta_corrente, "%.2f", saldo_conta);
  fclose(saldo_conta_corrente);
}

// Funcao para o usuario comprar um produto da loja do nosso banco
void loja() {
  printf("\033[92mLoja GUILO BANK\033[0m\n");
  while (1) {
    printf("-------------------------\n");
    printf("A loja de vantagens do GUILO BANK\n\n");
    printf(" 1 - Gift Card Spotify    R$17,00 (1 mes)\n"
           " 2 - Gift Card MAC FEI    R$20,00 (1 mes)\n"
           " 3 - Souvenir Robo FEI    R$6,00  (1 und)\n\n"
           " 0 - Voltar ao menu \n\n");
    int produto;
    scanf("%d", &produto);
    if (produto == 1) {
      produtos_loja("Gift Card", "Spotify", 17);
    } else if (produto == 2) {
      produtos_loja("Gift Card", "MAC FEI", 20);
    } else if (produto == 3) {
      produtos_loja("Souvenir", "Robô", 6);
    } else if (produto == 0) {
      return;
    } else {
      printf("Opcao invalida");
      return;
    }
  }
}

// Funcao para criar o menu interativo com o usuario
void menu() {
  while (1) {
    printf("\n\n-------------------------\n");
    printf("\033[92mMenu GUILO BANK\033[0m\n");
    printf("-------------------------\n"
           "O que deseja fazer?\n\n"
           " 1 - Conta Corrente  \n"
           " 2 - Poupanca \n"
           " 3 - Transferencia\n"
           " 4 - Cadastro de Receitas e Gastos\n"
           " 5 - Relatorio de transacao \n"
           " 6 - Investimento \n"
           " 7 - Emprestimo  \n"
           " 8 - Cartao Online \n"
           " 9 - Loja\n\n"
           " 0 - Sair\n\n");
    int option;
    scanf("%d", &option);
    printf("\n-------------------------\n");
    if (option == 1)
      conta_corrente();
    else if (option == 2)
      poupanca();
    else if (option == 3)
      transferencia();
    else if (option == 4)
      receita_gasto();
    else if (option == 5)
      rel_transacao();
    else if (option == 6)
      investimento();
    else if (option == 7)
      emprestimo_bancario();
    else if (option == 8)
      cartao_online();
    else if (option == 9)
      loja();
    else if (option == 0) {
      printf("Muito obrigado! Volte Sempre!\n");
      exit(0);
    } else {
      printf("\033[92mDigite uma opcao valida!\033[0m\n");
      printf("-------------------------\n");
    }
  }
}

// Funcao main para colocar acentos e cedilhas, alem de chamar a funcao
// entrar_conta(), que e o comeco do programa
int main() {
  setlocale(LC_ALL, "portuguese");
  srand((unsigned)time(NULL));
  entrar_conta();
  menu();
  return 0;
}