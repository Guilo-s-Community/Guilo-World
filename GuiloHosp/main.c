#include <locale.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TAM 20

const char *ARQUIVO_CADASTRO = "cadastro.txt";
const char *ARQUIVO_SEGURANCA = "senha.txt";

typedef struct data {
  int dia, mes, ano;
} data;

typedef struct registro {
  int idade;
  char nome[20];
  data entrada;
  char rg[10];
} registro;

typedef struct Vertice {
  int valor;
  struct Vertice *esq;
  struct Vertice *dir;
  struct Vertice *pai;
} Vertice;

typedef struct Celula {
  int value;
  registro valor;
  struct Celula *proximo;
  struct Celula *anterior;
} Celula;

typedef struct Lista {
  int qtde;
  Celula *primeiro;
} Lista;

typedef struct Efila {
  registro dados;
  struct Efila *proximoFila;
  struct Efila *anteriorFila;
} Efila;

typedef struct Fila {
  int qtde;
  Efila *head, *tail;
} Fila;

void inserirLista(Lista *l, registro valorNovo) {
  Celula *celula = (malloc(sizeof(Celula)));
  celula->proximo = l->primeiro;
  celula->valor = valorNovo;
  l->primeiro = celula;
  l->qtde++;
}

void removerPaciente(Lista *l, char *nome) {
  Celula *atual = l->primeiro;
  Celula *anterior = NULL;

  while (atual != NULL) {
    if (strcmp(nome, atual->valor.nome) == 0) {
      if (anterior == NULL) {
        l->primeiro = atual->proximo;
      } else {
        anterior->proximo = atual->proximo;
      }
      free(atual);
      l->qtde--;
      break;
    }
    anterior = atual;
    atual = atual->proximo;
  }
}

void atualizaPaciente(Lista *l, char *nome) {
  int opcao, novaIdade;
  Celula *atual = l->primeiro;
  Celula *anterior = NULL;
  char novoNome[TAM];

  atual = l->primeiro;
  anterior = NULL;

  while (atual != NULL) {
    if (strcmp(nome, atual->valor.nome) == 0) {
      printf("Escolha uma das opções para atualizar\n");
      printf("1 - Nome\n2 - RG\n3 - Idade\n0 - Voltar\n");
      scanf("%d", &opcao);
      getchar();
      if (opcao == 1) {
        printf("\nDigite o nome atualizado do paciente\n");
          fgets(novoNome, 100, stdin);
          sscanf(novoNome, "%[^\n]s", novoNome);
        strcpy(atual->valor.nome, novoNome);
        printf("Nome %s atualizado com sucesso\n", atual->valor.nome);

      } else if (opcao == 2) {
        printf("Digite o RG atualizado do paciente\n");
          fgets(novoNome, 100, stdin);
          sscanf(novoNome, "%[^\n]s", novoNome);
        strcpy(atual->valor.rg, novoNome);
        printf("RG %s atualizado com sucesso\n", atual->valor.rg);

      } else if (opcao == 3) {
        printf("Digite a idade atualizada do paciente\n");
          fgets(novoNome, 100, stdin);
          sscanf(novoNome, "%[^\n]s", novoNome);
          atual->valor.idade = strtol(novoNome, NULL, 10);
        printf("Idade atualizada com sucesso\n");

      } else if (opcao == 0) {
        return;
      } else {
        printf("Digite uma opção válida!");
      }
      return;
    }
    anterior = atual;
    atual = atual->proximo;
  }
}

Lista *inicializa_lista() {
  Lista *l = malloc(sizeof(Lista));
  l->primeiro = NULL;
  l->qtde = 0;
  return l;
}

void imprimirLista(Lista *l) {
  Celula *atual = l->primeiro;
  Celula *anterior = NULL;

  printf("end-> [ ");
  while (atual != NULL) {
    printf("| %s ", atual->valor.nome);
    anterior = atual;
    atual = atual->proximo;
  }
  printf("] <-start\n");
  printf("Total de pacientes: %d\n", l->qtde);
}

void verPaciente(Lista *l, char *paciente) {
  Celula *atual = l->primeiro;
  Celula *anterior = NULL;
  while (atual != NULL) {
    if (strcmp(atual->valor.nome, paciente) == 0) {
      printf("Nome: %s\n", atual->valor.nome);
      printf("RG: %s\n", atual->valor.rg);
      printf("Idade: %d\n", atual->valor.idade);
      printf("Data de registro: %d/%d/%d\n", atual->valor.entrada.dia,
             atual->valor.entrada.mes, atual->valor.entrada.ano);
      break;
    }
    anterior = atual;
    atual = atual->proximo;
  }
}

Efila *cria_celula(registro valorNovo) {
  Efila *efila = malloc(sizeof(Efila));
  efila->proximoFila = NULL;
  efila->dados = valorNovo;

  return efila;
}

Fila *cria_queue() {
  Fila *queue = malloc(sizeof(Fila));
  queue->head = NULL;
  queue->tail = NULL;
  queue->qtde = 0;
  return queue;
}

void enfileirarPaciente(Fila *queue, char *paciente, Lista *l) {
    Celula *atual = l->primeiro;
    Celula *anterior = NULL;

    while (atual != NULL) {
        if (strcmp(paciente, atual->valor.nome) == 0) {
            printf("Found %s", paciente);
            break;
        } else {
        }

        atual = atual->proximo;
    }

    if (atual != NULL) {
        Efila *nova = cria_celula(atual->valor);
        if (queue->qtde == 0) {
            queue->head = nova;
            queue->tail = nova;
        } else {
            queue->tail->proximoFila = nova;
            queue->tail = nova;
        }
        queue->qtde++;
    }
    else {
        return;
    }
}

int dequeue(Fila *queue){
  if(queue->head != NULL){
    int valor = 1;
    Celula *head = queue->head;
    queue->head = queue->head->proximoFila;
    queue->head->anteriorFila = NULL;
    if(queue->qtde == 1){
      queue->tail = NULL;
    }
    queue->qtde--;
    free(head);
    return valor;
  } else {
    return -1;
  }
}

void desenfileirarPaciente(Fila *queue) {
    int result = dequeue(queue);
    if (result != -1) {
        printf("Paciente desenfileirado!");
    } else {
        printf("Erro");
    }
}

void show(Fila *queue) {
  Efila *anteriorFila = NULL;
  Efila *atualFila = queue->head;
  printf("[");
  while (atualFila != NULL) {
    printf("| %s ", atualFila->dados.nome);
    atualFila = atualFila->proximoFila;
  }
  printf("]\n");
  printf("Número de pacientes na fila: %d\n", queue->qtde);
}

void cria_arquivo_se_nao_existe(const char *nome_arquivo) {
  FILE *file = fopen(nome_arquivo, "r");
  if (file) {
    fclose(file);
  } else {
    FILE *file = fopen(nome_arquivo, "a");
    fclose(file);
  }
}

void criptografia() {
  // SENHA É "admin"
  cria_arquivo_se_nao_existe(ARQUIVO_SEGURANCA);
  char senha[255], senha_salva[255];
  int i = 0;
  while (1) {
    printf("\n\n-------------------------\n");
    printf("\033[92mBem Vindo ao programa do HospFEI \033[0m\n");
    printf("-------------------------\n");
    printf("Digite a sua senha de admin\n");
    scanf("%s", senha);
    FILE *seguranca = fopen(ARQUIVO_SEGURANCA, "r+");
    fscanf(seguranca, "%s", senha_salva);
    if (strcmp(senha_salva, senha) == 0) {
      break;
    } else {
      printf("Senha incorreta!\n");
      i++;
      printf("Você tem 3 tentativas, esta é a sua %dª tentaviva\n", i);
    }
    if (i == 3) {
      printf("\n\033[91mPrograma Bloqueado por inúmeras tentativas\n"
             "Entre em contato com o suporte técnico.\033[91m\n");
      exit(0);
    }
  }
}

int cadastrar(Lista *l) {
  Celula *atual;
  char escolhaNome[TAM];
  char aux[100];
  cria_arquivo_se_nao_existe(ARQUIVO_CADASTRO);

  while (1) {
    printf("\n\033[92mCadastro \033[0m\n");
    printf("-------------------------\n"
           "O que deseja fazer?\n\n"
           " 1 - Cadastrar novo paciente \n"
           " 2 - Consultar paciente cadastrado \n"
           " 3 - Mostrar lista completa\n"
           " 4 - Atualizar dados de paciente\n"
           " 5 - Remover paciente\n"
           " 0 - Voltar\n\n");
    int option;
    scanf("%d", &option);
    getchar();

    if (option == 1) {
      registro c;
      FILE *f;
      f = fopen("cadastro.txt", "a");
      printf("Qual o nome do paciente?  ");
      fgets(aux, 100, stdin);
      sscanf(aux, "%[^\n]s", aux);
      strcpy(c.nome, aux);
      printf("Qual é a idade do paciente?  ");
      fgets(aux, 100, stdin);
      sscanf(aux, "%[^\n]s", aux);
      c.idade = strtol(aux, NULL, 10);
      printf("Qual é o RG do paciente?  ");
      fgets(aux, 100, stdin);
      sscanf(aux, "%[^\n]s", aux);
      strcpy(c.rg, aux);
      // c.rg[strcspn(c.rg, "\n")] = 0;
      printf("Qual dia do cadastro? ");
      fgets(aux, 100, stdin);
      sscanf(aux, "%[^\n]s", aux);
      c.entrada.dia = strtol(aux, NULL, 10);
      printf("Qual mes do cadastro? ");
        fgets(aux, 100, stdin);
        sscanf(aux, "%[^\n]s", aux);
        c.entrada.mes = strtol(aux, NULL, 10);
      printf("Qual ano do cadastro? ");
        fgets(aux, 100, stdin);
        sscanf(aux, "%[^\n]s", aux);
        c.entrada.ano = strtol(aux, NULL, 10);
      printf("---------------------------\n");

      fprintf(f, "Ordem de registro: %d |", l->qtde);
      fprintf(f, "Nome: %s |", c.nome);
      fprintf(f, "Idade: %d |", c.idade);
      fprintf(f, "RG: %s |", c.rg);
      fprintf(f, "Data de Registro: %d/%d/%d |\n", c.entrada.dia, c.entrada.mes,
              c.entrada.ano);
      fclose(f);
      inserirLista(l, c);

    } else if (option == 2) {
      Celula *atual = l->primeiro;
      Celula *anterior = NULL;
      char paciente[TAM];
      printf("Escolha o paciente a ser consultado:\n");
      printf("[ ");
      while (atual != NULL) {
        printf(" |%s", atual->valor.nome);
        anterior = atual;
        atual = atual->proximo;
      }
      printf(" ]\n");
      fgets(paciente, 100, stdin);
      sscanf(paciente, "%[^\n]s", paciente);
      verPaciente(l, paciente);
    } else if (option == 3) {
      imprimirLista(l);
      printf("---------------------------");
    } else if (option == 4) {
      char atualizacao[100];
      printf("Digite o nome do paciente que deseja atualizar: \n");
      fgets(atualizacao, 100, stdin);
      sscanf(atualizacao, "%[^\n]s", atualizacao);
      atualizaPaciente(l, atualizacao);
      printf("Paciente atualizado com sucesso!\n");
    } else if (option == 5) {
      char remocao[100];
      printf("Qual o nome do paciente que deseja remover?\n");
      fgets(remocao, 100, stdin);
      sscanf(remocao, "%[^\n]s", remocao);
      removerPaciente(l, remocao);
      printf("Paciente %s removido com sucesso!\n", remocao);
    } else if (option == 0) {
      return 0;
    }
  }
}

int atendimento(Lista *l, Fila *queue) {
  char escolhaNome[TAM];
  registro q;
  while (1) {
    printf("\n\n-------------------------\n");
    printf("\033[92mAtendimento \033[0m\n");
    printf("-------------------------\n"
           "O que deseja fazer?\n\n"
           " 1 - Enfileirar Paciente \n"
           " 2 - Desenfileirar Paciente \n"
           " 3 - Mostrar fila completa\n"
           " 0 - Voltar\n\n");
    int option;
    scanf("%d", &option);
    getchar();
    if (option == 1) {
      printf("Escreva o nome do paciente a ser colocado na fila:\n");
        fgets(escolhaNome, 100, stdin);
        sscanf(escolhaNome, "%[^\n]s", escolhaNome);
      enfileirarPaciente(queue, escolhaNome, l);
    } else if (option == 2) {
        desenfileirarPaciente(queue);
    }
    else if (option == 3)
      show(queue);
    else if (option == 0)
      return 0;
  }
}

int carregarsalvar(Lista *l) {
    while (1) {
        printf("\n\n-------------------------\n");
        printf("\033[92mCarregar / Salvar \033[0m\n");
        printf("-------------------------\n"
               "O que deseja fazer?\n\n"
               " 1 - Salvar Lista \n"
               " 2 - Carregar Lista \n"
               " 0 - Voltar\n\n");
        int option;
        scanf("%d", &option);
        getchar();
        if (option == 1) {
            cria_arquivo_se_nao_existe("salvei.bin");
            FILE *f;
            f = fopen("salvei.bin", "wb");

            Celula *atual = l->primeiro;
            while (atual != NULL) {
                fwrite(&atual->valor, sizeof(registro), 1, f);
                atual = atual->proximo;
            }

            fclose(f);

            printf("Sucesso salvar");

        } else if (option == 2) {
            cria_arquivo_se_nao_existe("salvei.bin");
            FILE *f;
            f = fopen("salvei.bin", "rb");

            registro c;
            while (fread(&c, sizeof(registro), 1, f) != 0) {
                inserirLista(l,c);
            }

            printf("Sucesso carregar");
        }
        else if (option == 0)
            return 0;
    }
}

int pesquisa() {
  while (1) {
    printf("-------------------------\n"
           "O que deseja fazer?\n\n"
           " 1 - Mostrar registros ordenados por ano de registro \n"
           " 2 - Mostrar registros ordenados por mês de registro \n"
           " 3 - Mostrar registros ordenados por dia de registro\n"
           " 4 - Mostrar registros ordenados por idade do paciente\n"
           " 0 - Voltar\n\n");
    int option;
    scanf("%d", &option);
    if (option == 1) {

    } else if (option == 2)
      printf("a");
    else if (option == 3)
      printf("a");
    else if (option == 4)
      printf("a");
    else if (option == 0)
      return 0;
  }
}

void sobre() {
  printf("\033[92mNome dos Programadores \033[0m\n"
         "Paulo Vinicius Araujo Feitosa\nGuilherme Marcato Mendes Justiça\n"
         "Ciclo:      Vespertino\n"
         "Curso:      Ciencia da Computacao\n"
         "Data:       17/11/2023\n"
         "Disciplina: CC4652");
}

void menu(Lista *l, Fila *queue) {
  while (1) {
    printf("\n\n-------------------------\n");
    printf("\033[92mMenu HOSPITAL HospFEI \033[0m\n");
    printf("-------------------------\n"
           "O que deseja fazer?\n\n"
           " 1 - Cadastrar Paciente \n"
           " 2 - Atendimento \n"
           " 3 - Pesquisar Registro\n"
           " 4 - Carregar/Salvar Arquivo\n"
           " 5 - Sobre os Programadores\n"
           " 0 - Sair\n\n");
    int option;
    scanf("%d", &option);
    printf("\n-------------------------");
    if (option == 1)
      cadastrar(l);
    else if (option == 2)
      atendimento(l, queue);
    else if (option == 3)
      printf("a");
    else if (option == 4)
      carregarsalvar(l);
    else if (option == 5)
      sobre();
    else if (option == 0) {
      printf("\nPrograma encerrado!");
      exit(0);
    } else {
      printf("\033[92mDigite uma opção válida!\033[0m\n");
      printf("-------------------------\n");
    }
  }
}

int main(int argc, char *argv[]) {
  criptografia();
  Lista *l = inicializa_lista();
  Fila *queue = cria_queue();
  menu(l, queue);
  return 0;
}
