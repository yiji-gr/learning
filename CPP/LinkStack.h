#pragma once
#include <iostream>
#include "node.h"
using namespace std;

class LinkStack {
private:
	int len;
	node *bottom;
	node *top;
public:
	LinkStack() {
		bottom = new node(-1);
		top = bottom;
		len = 0;
	}
	~LinkStack()
	{
		node *n = new node(-1);
		while (bottom != NULL) {
			n = bottom;
			bottom = bottom->next;
			delete n;
		}
		n = NULL;
	}

	void push(int num) {
		node *n = new node(num);
		n->next = bottom->next;  //头插法
		bottom->next = n;
		top = n;
		len++;
	}

	int pop() {
		if (top == bottom)
		{
			cout << "stack is empty!" << endl;
			return -1;
		}

		node *n = top;
		bottom->next = n->next;
		top = bottom->next;

		int num = n->data;
		delete n;
		n = NULL;
		len--;

		if (bottom->next == NULL)
			top = bottom;

		return num;
	}

	void print() {
		node *n = bottom->next;
		while (n != NULL) {
			cout << n->data << " ";
			n = n->next;
		}
		cout << endl;
	}
};

//int main()
//{
//	LinkStack q;
//	for (int i = 0; i < 3; ++i) {
//		q.push(i);
//		q.print();
//	}
//	for (int i = 0; i < 3; ++i) {
//		q.pop();
//		q.print();
//	}
//
//	return 0;
//}
