#pragma once
#include <iostream>
using namespace std;

class SeStack {
private:
	int len;
	int *data;
	int top;
public:
	SeStack(int n) {
		data = new int[n];
		top = 0;
		len = n;
	}
	~SeStack()
	{
		delete[]data;
	}

	void push(int num) {
		if (top == len)
		{
			cout << "stack is full!" << endl;
			return;
		}
		data[top++] = num;
	}

	int pop() {
		if(top == 0)
		{
			cout << "stack is empty!" << endl;
			return -1;
		}

		return data[top--];
	}

	int get_top() {
		if (top != 0)
			return data[top - 1];
		cout << "stack is empty!" << endl;
		return -1;
	}

	void print() {
		for (int i = 0; i < top; ++i)
			cout << data[i] << " ";
		cout << endl;
	}
};

//int main()
//{
//	SeStack q(10);
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
