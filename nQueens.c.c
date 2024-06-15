#include <stdio.h>
#include <stdlib.h>

//Protótipo das funções
void resolveCol(int);   //resolve a Coluna
int ehSeguro(int, int); //Verifica se é seguro
void printTab();        //Printa o tabuleiro
void solucao();         //Chamada da solução

//Variaveis globais
int N;                 //N (tamanho do tabuleiro)
int tabuleiro[32][32]; //Tabuleiro com dimensões máximas
int temSolucao = 0;    //Verifica se o problema já foi solucionado
int nSol = 0;

int main()
{
    //Entrada de valores
    FILE *rainha; //File rainha onde vão ser gravados os dados
    FILE *limpa;  //File limpa, limpa o arquivo gerado na ultima execução
    limpa = fopen("rainha.out", "w");
    fclose(limpa);
    rainha = fopen("rainha.out", "a"); //Uso do append para não apagar dados do arquivo
    printf("Digite o tamanho do tabuleiro N (NxN) \n");
    scanf("%d", &N);
    solucao();
    fseek(rainha, 0, SEEK_SET);      //Seta para o começo do arquivo
    fprintf(rainha, "%d\n\n", nSol); //Printa o numero de soluções encontradas
    fclose(rainha);
    return 0;
}

void printTab()
{
    FILE *rainha;                      //File rainha onde serao gravados os dados
    rainha = fopen("rainha.out", "a"); //file em append para não apagar os dados da ultima solução
    for (int i = 0; i < N; i++)        //Loop normal para printar
    {
        for (int j = 0; j < N; j++)
        {
            if (tabuleiro[i][j] == 1)
            {
                fprintf(rainha, "1 ");
            }

            else
            {
                fprintf(rainha, "0 ");
            }
        }
        fprintf(rainha, "\n");
    }
    fprintf(rainha, "\n\n"); //Dá os dois espaços entre cada resolução
}

void solucao()
{
    //inicia em 0,0
    resolveCol(0);
    if (temSolucao == 0)
        printf("Sem solução \n");
}

void resolveCol(int col)
{
    //Se coluna == N significa que a solução foi encontrada
    if (col == N)
    {
        temSolucao = 1;
        nSol++;
        printTab(); //Função para printar no arquivo final
        //return para procurar novas soluções
        return;
    }

    for (int i = 0; i < N; i++) //Linha em linha
    {
        if (ehSeguro(i, col) == 1) //função ehSeguro verifica se é seguro colocar uma rainha ali
        {
            tabuleiro[i][col] = 1; //Coloca a rainha
            resolveCol(col + 1);   //Avança para a proxima coluna e continua a recursão
            tabuleiro[i][col] = 0; //Remove a rainha se "der errado"
        }
    }
}

int ehSeguro(int row, int col)
{

    //checa a linha
    for (int i = col; i >= 0; i--) //i-- porque a verificação vem da esquerda
    {
        if (tabuleiro[row][i] == 1)
            return 0;
    }

    //Checa diagonal esquerda
    for (int i = row, j = col; i >= 0 && j >= 0; i--, j--)
    {
        if (tabuleiro[i][j] == 1)
            return 0;
    }

    //Checa diagonal direita
    for (int i = row, j = col; i < N && j >= 0; i++, j--)
    {
        if (tabuleiro[i][j] == 1)
            return 0;
    }

    return 1;
}