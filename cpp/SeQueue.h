#pragma once
#include <iostream>
using namespace std;

class SeQueue {
private:
	int front;
	int rear;
	int len;
	int *data;
public:
	SeQueue(int n) {
		data = new int[n];
		front = 0;
		rear = 0;
		len = n;
	}
	~SeQueue() {
		delete []data;
	}

	void enqueue(int num) {
		if (rear == len) {
			if (front == 0) {
				cout << "queue is full!" << endl;
				return;
			}

			for (int i = front; i < len; i++)
				data[i - front] = data[i];
			rear -= front;
			front = 0;
		}

		data[rear++] = num;
	}

	int dequeue() {
		if (rear == front) {
			cout << "queue is empty" << endl;
			return -1;
		}

		front++;
		return data[front - 1];
	}

	void print() {
		for (int i = front; i < rear; ++i)
			cout << data[i] << " ";
		cout << endl;
	}
};

//int main()
//{
//	SeQueue q(10);
//	for (int i = 0; i < 3; ++i) {
//		q.enqueue(i);
//		q.print();
//	}
//	for (int i = 0; i < 3; ++i) {
//		q.dequeue();
//		q.print();
//	}
//
//	return 0;
//}
