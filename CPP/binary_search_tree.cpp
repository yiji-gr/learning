#include <iostream>
#include <vector>
#include <string>

using namespace std;

template<class T>
struct Node {
	Node<T>* left = nullptr;
	Node<T>* right = nullptr;
	T val;
	Node(T v) :val(v) {}
	Node() {}
};

template<class T>
class BSTree {
public:
	BSTree() {
		head = new Node<T>;
	}
	~BSTree() {
		release(root);
	}
	void preOrder();
	void preOrder(Node<T>* rt);
	void inOrder();
	void inOrder(Node<T>* rt);
	void postOrder();
	void postOrder(Node<T>* rt);
	void insert(T num);
	void del(T num);
	int search(T num);
	void release(Node<T>* rt);
private:
	Node<T>* head;
	Node<T>* root;
	int length = 0;
};

template<class T>
void BSTree<T>::release(Node<T>* rt) {
	if (rt == nullptr)
		return;
	release(rt->left);
	release(rt->right);
	delete rt;
}

template<class T>
void BSTree<T>::insert(T num) {
	if (length == 0) {
		root = new Node<T>(num);
		head->left = root;
	}
	else {
		Node<T>* tmp = root;
		while (tmp != nullptr) {
			if (tmp->val == num) {
				string error = "the node is already existed!";
				cout << error << endl;
				throw error;
			}
			else if (tmp->val > num) {
				if (tmp->left == nullptr) {
					Node<T>* node = new Node<T>(num);
					tmp->left = node;
					break;
				}
				tmp = tmp->left;
			}
			else {
				if (tmp->right == nullptr) {
					Node<T>* node = new Node<T>(num);
					tmp->right = node;
					break;
				}
				tmp = tmp->right;
			}
		}
	}
	length++;
}

template<class T>
void BSTree<T>::del(T num) {
	if (length == 0) {
		string error = "the binary search tree is empty!";
		cout << error << endl;
		throw error;
	}
	else {
		Node<T>* cur_child = head->left;
		Node<T>* cur_parent = head;
		int is_left = 0;	// 0 根节点 1 左儿子 2 右儿子
		while (cur_child != nullptr) {
			if (cur_child->val > num) {		// 大于当前值就从左子树中找
				if (cur_child->left == nullptr) {
					cout << "the node to delete is not existed" << endl;
					return;
				}
				cur_parent = cur_child;
				cur_child = cur_child->left;
				is_left = 1;
			}
			else if (cur_child->val < num) {		// 小于当前值就从右子树中找
				if (cur_child->right == nullptr) {
					cout << "the node to delete is not existed" << endl;
					return;
				}
				cur_parent = cur_child;
				cur_child = cur_child->right;
				is_left = 2;
			}
			else {		// 找到了
				length--;
				if (cur_child->right == nullptr) {		//右子树为空，直接父节点连左子树
					if (is_left == 1)
						cur_parent->left = cur_child->left;
					else if (is_left == 2)
						cur_parent->right = cur_child->left;
					else {		//根节点另外判断
						root = cur_child->left;
						head->left = root;
					}
					delete cur_child;
					return;
				}
				else if (cur_child->right->left == nullptr) {	//右子树的左儿子为空，直接父节点连右子树，右子树连当前节点左儿子
					Node<T>* node = cur_child->right;
					if (is_left == 1)
						cur_parent->left = node;
					else if (is_left == 2)
						cur_parent->right = node;
					else {		//根节点另外判断
						node->left = cur_child->left;
						root = node;
						head->left = root;
					}
					node->left = cur_child->left;
					delete cur_child;
					return;
				}
				else if (cur_child->right->left != nullptr) {	//右子树的左儿子不为空，递归到右子树最后一个左儿子n，取代当前节点，父节点连n，n左右子树为当前节点左右子树
					Node<T>* tmp_parent = cur_child->right;
					Node<T>* tmp_child = cur_child->right->left;
					while (tmp_child->left != nullptr) {
						tmp_parent = tmp_child;
						tmp_child = tmp_child->left;
					}
					if (tmp_child->right != nullptr)		//n右子树不存在则n的父节点左儿子为n的右子树， n右子树不存在则n的父节点左儿子为空
						tmp_parent->left = tmp_child->right;
					else
						tmp_parent->left = nullptr;
					tmp_child->left = cur_child->left;
					tmp_child->right = cur_child->right;
					if (is_left == 1)
						cur_parent->left = tmp_child;
					else if (is_left == 2)
						cur_parent->right = tmp_child;
					else {		//根节点另外判断
						root = tmp_child;
						head->left = root;
					}
					delete cur_child;
					return;
				}
			}
		}
	}
}

template<class T>
int BSTree<T>::search(T num) {
	if (length == 0) {
		return -1;
	}
	Node<T>* node = root;
	while (node != nullptr) {
		if (node->val == num)
			return 1;
		else if (node->val > num)
			node = node->left;
		else
			node = node->right;
	}
	return -1;
}

template<class T>
void BSTree<T>::preOrder(Node<T>* rt) {
	if (!rt)
		return;
	cout << rt->val << " ";
	preOrder(rt->left);
	preOrder(rt->right);
}

template<class T>
void BSTree<T>::preOrder() {
	cout << "-------    preOrder    -------" << endl;
	preOrder(this->root);
	cout << endl;
}

template<class T>
void BSTree<T>::inOrder(Node<T>* rt) {
	if (!rt)
		return;
	inOrder(rt->left);
	cout << rt->val << " ";
	inOrder(rt->right);
}

template<class T>
void BSTree<T>::inOrder() {
	cout << "-------    inOrder    -------" << endl;
	inOrder(this->root);
	cout << endl;
}

template<class T>
void BSTree<T>::postOrder(Node<T>* rt) {
	if (!rt)
		return;
	postOrder(rt->left);
	postOrder(rt->right);
	cout << rt->val << " ";
}

template<class T>
void BSTree<T>::postOrder() {
	cout << "-------    postOrder    -------" << endl;
	postOrder(this->root);
	cout << endl;
}

int main() {
	BSTree<float> bst;
	vector<float> a = { 6,3,5,1,7,2,6.5,9,4,8,0 };
	for (int i = 0; i < a.size(); ++i) {
		bst.insert(a[i]);
	}

	bst.del(6);

	bst.preOrder();
	bst.inOrder();
	bst.postOrder();
	return 0;
}
