#include<stdio.h>
#include<stdlib.h>

typedef struct node			// 单链表
{
	int age;
	char name[20];
	struct node *next;
} Node, *Linklist;

Linklist Insert_Linklist()		// 链表插入 尾插法
{
	Node *head, *cur, *p;
	head = (Node *)malloc(sizeof(Node));
	head->next = NULL;
	cur = head;

	int age;
	scanf("%d", &age);
	while(age != -1)
	{
		p = (Node*)malloc(sizeof(Node));
		scanf("%s", p->name);
		p->age = age;
		cur->next = p;
		cur = p;
		scanf("%d", &age);
	}
	cur->next = NULL;

	return head;
}

void Print_Linklist(Linklist list)	// 打印链表所有元素
{
	Node *start;
	for(start = list->next; start != NULL; start = start->next)
	{
		printf("%d %s\n", start->age, start->name);
	}
}

Linklist Del_Linklist(Linklist list, int age)	// 按信息删除对应节点
{
	Node *p, *cur;
	p = list->next;
	while(p->age != age)
	{
		cur = p;
		p = p->next;
	}
	cur->next = p->next;
	free(p);

	return list;
}

int main()
{
	Linklist list;

	list = Insert_Linklist();

	Print_Linklist(list);

	int age = 1;
	list = Del_Linklist(list, age);

	printf("**********");
	Print_Linklist(list);

	return 0; 
}
