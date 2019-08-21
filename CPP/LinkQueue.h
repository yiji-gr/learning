#pragma once
#include "node.h"
#include <iostream>
using namespace std;

class LinkQueue {
private:
	node *front;
	node *rear;
	int len;
public:
	LinkQueue() {
		front = new node(-1);
		rear = front;
		len = 0;
	}
	~LinkQueue()
	{
		node *n = new node(-1);
		while (front != NULL) {
			n = front;
			front = front->next;
			delete n;
		}
		n = NULL;
	}

	void enqueue(int num) {
		node *n = new node(num);
		rear->next = n;			//尾插法
		rear = n;
		len++;
	}

	int dequeue() {
		if (front == rear)
		{
			cout << "queue is empty" << endl;
			return -1;
		}

		node *n = front->next;
		front->next = n->next;
		if (n == rear)
			rear = front;

		int num = n->data;
		delete n;
		n = NULL;
		len--;
		return num;
	}

	void print() {
		node *n = front->next;
		while (n != NULL)
		{
			cout << n->data << " ";
			n = n->next;
		}
		cout << endl;
	}
};

//int main()
//{
//	LinkQueue q;
//	for (int i = 0; i < 3; ++i) {
//		q.enqueue(i);
//		q.print();
//	}
//
//	for (int i = 0; i < 3; ++i) {
//		q.dequeue();
//		q.print();
//	}
//	return 0;
//}
