#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <string>
#include <random>

using namespace std;

class Sort {
public:
	Sort() {}
	Sort(vector<int> arrs){
		data.assign(arrs.begin(), arrs.end());
		len = data.size();
	}
	virtual vector<int> sort() = 0;

	void print(vector<int> arrs, string mode="") {
		cout << "------------\t" + mode + "\t----------" << endl;
		for (auto i : arrs)
			cout << i << " ";
		cout << endl;
		cout << "------------end----------" << endl << endl;
	}

	void swap(int &a, int &b) {   // 当a,b为同一地址时，函数结束a=b=0 
		a = a ^ b;
		b = a ^ b;
		a = a ^ b;
	}

	int max_(vector<int> arrs) {
		int max_num = arrs[0];
		for (int i = 0; i < arrs.size(); ++i) {
			if (max_num < arrs[i])
				max_num = arrs[i];
		}
		return max_num;
	}

	int min_(vector<int> arrs) {
		int min_num = arrs[0];
		for (int i = 0; i < len; ++i) {
			if (min_num > arrs[i])
				min_num = arrs[i];
		}
		return min_num;
	}

private:
	vector<int> data;
	int len;
};

class BubbleSort :public Sort {
public:
	BubbleSort(vector<int> arrs) {
		data.assign(arrs.begin(), arrs.end());
		len = data.size();
	}

	vector<int> sort() {
		for (int i = 0; i < len - 1; ++i) {
			for (int j = i + 1; j < len; ++j) {
				if (data[i] > data[j]) {
					swap(data[i], data[j]);
				}
			}
		}
		return data;
	}
private:
	vector<int> data;
	int len;
};

class SelectionSort :public Sort {
public:
	SelectionSort(vector<int> arrs) {
		data.assign(arrs.begin(), arrs.end());
		len = arrs.size();
	}

	vector<int> sort() {
		for (int i = 0; i < len - 1; ++i) {
			int min_num = data[i], min_idx = i;
			for (int j = i + 1; j < len; ++j) {
				if (min_num > data[j]) {
					min_idx = j;
					min_num = data[j];
				}
			}
			if(i != min_idx)		// ---------------
				swap(data[i], data[min_idx]);
		}
		return data;
	}
private:
	vector<int> data;
	int len;
};

class InsertionSort :public Sort {
public:
	InsertionSort(vector<int> arrs){
		 data.assign(arrs.begin(), arrs.end());
		 len = arrs.size();
	 }
	 vector<int> sort() {
		 for (int i = 1; i < len; ++i) {
			 int cur = i;
			 for (int j = i - 1; j >= 0; j--) {
				 if(data[cur] < data[j]){
					 swap(data[cur], data[j]);
					 cur--;
				 }
			 }
		 }
		 return data;
	 }
private:
	vector<int> data;
	int len;
};

class ShellSort :public Sort {
public:
	ShellSort(vector<int> arrs) {
		data.assign(arrs.begin(), arrs.end());
		len = arrs.size();
	}
	vector<int> sort() {
		int gap = len / 2;
		while (gap >= 1) {
			for (int i = gap; i < len; i += gap) {
				int cur = i;
				for (int j = cur - gap; j >= 0; j -= gap) {
					if (data[cur] < data[j]) {
						swap(data[cur], data[j]);
						cur -= gap;
					}
				}
			}
			gap /= 2;
		}

		return data;
	}
private:
	vector<int> data;
	int len;
};

class MergeSort :public Sort {
public:
	MergeSort(vector<int> arrs) {
		data.assign(arrs.begin(), arrs.end());
		len = arrs.size();
	}

	vector<int> sort() {
		return mergesort(0, len);
	}

	vector<int> mergesort(int low, int high) {
		if (high - low == 1)
			return{ data[low] };
		int mid = (high + low) / 2;
		return merge(mergesort(low, mid), mergesort(mid, high));
	}

	vector<int> merge(vector<int> arr1, vector<int> arr2) {
		vector<int> arrs;
		for (int i = 0, j = 0; i < arr1.size() || j < arr2.size();) {
			if (i >= arr1.size())
				arrs.push_back(arr2[j++]);
			else if (j >= arr2.size())
				arrs.push_back(arr1[i++]);
			else if (arr1[i] > arr2[j])
				arrs.push_back(arr2[j++]);
			else
				arrs.push_back(arr1[i++]);
		}

		return arrs;
	}
private:
	vector<int> data;
	int len;
};

class QuickSort :public Sort {
public:
	QuickSort(vector<int> arrs) {
		data.assign(arrs.begin(), arrs.end());
		len = arrs.size();
	}

	vector<int> sort() {
		quicksort(0, len - 1);
		return data;
	}

	void quicksort(int low, int high) {
		if (low < high) {
			int pivot = partition(low, high);
			quicksort(low, pivot - 1);
			quicksort(pivot + 1, high);
		}
	}

	int partition(int low, int high) {
		int tmp = data[low];
		while (low < high) {
			while (low < high && data[high] >= tmp)
				high--;
			if (low < high)
				data[low++] = data[high];
			while (low < high && data[low] < tmp)
				low++;
			if (low < high) 
				data[high--] = data[low];
		}
		data[low] = tmp;
		return low;
	}
private:
	vector<int> data;
	int len;
};

class HeapSort :public Sort {
public:
	HeapSort(vector<int> arrs) {
		data.assign(arrs.begin(), arrs.end());
		len = arrs.size();
	}

	vector<int> sort() {
		for (int i = 0; i < len - 1; ++i) {
			BuildMaxHeap(len - i);
			swap(data[0], data[len - i - 1]);
		}

		return data;
	}

	void BuildMaxHeap(int len_) {
		int num = len_ / 2 - 1;
		for (int i = num; i >= 0; --i) {
			int left = 2 * i + 1, right = 2 * i + 2;
			if (left < len_ && data[left] > data[i])
				swap(data[left], data[i]);
			if (right < len_ && data[right] > data[i])
				swap(data[right], data[i]);
		}
	}

private:
	vector<int> data;
	int len;
};

class CountingSort :public Sort {
public:
	CountingSort(vector<int> arrs) {
		data.assign(arrs.begin(), arrs.end());
		len = arrs.size();
		max_n = max_(data);
	}

	vector<int> sort() {
		vector<int> arrs(max_n + 1);
		for (int i = 0; i < max_n; ++i)
			arrs.push_back(0);

		for (auto each : data)
			arrs[each]++;

		vector<int> result;
		for (int i = 0; i <= max_n; ++i) {
			while (arrs[i] != 0) {
				result.push_back(i);
				arrs[i]--;
			}
		}
		return result;
	}
private:
	vector<int> data;
	int len;
	int max_n;
};

class BucketSort :public Sort {
public:
	BucketSort(vector<int> arrs) {
		data.assign(arrs.begin(), arrs.end());
		len = arrs.size();
		max_n = max_(data);
	}

	vector<int> sort() {
		vector<vector<int>> arrs;
		for (int i = 0; i < (max_n / base + 1); ++i) {
			vector<int> v;
			arrs.push_back(v);
		}

		for (int i = 0; i < len; ++i) {
			int num = data[i] / base;
			int j;
			for (j = 0; i < arrs[num].size(); ++j) {
				if (arrs[num][j] >= data[i])
					break;
			}
			arrs[num].insert(arrs[num].begin() + j, data[i]);
		}

		vector<int> result;
		for (auto rows : arrs)
			for (auto cols : rows)
				result.push_back(cols);

		return result;
	}
private:
	vector<int> data;
	int len;
	int min_n, max_n;
	int base = 10;
};

class RadixSort :public Sort {
public:
	RadixSort(vector<int> arrs) {
		data.assign(arrs.begin(), arrs.end());
		len = arrs.size();
		max_n = max_(data);
	}
	vector<int> sort() {
		int cnt = 0;
		while (max_n >= base) {
			max_n /= base;
			cnt++;
		}

		vector<vector<int>> arrs;
		for (int i = 0; i < cnt; ++i) {
			vector<int> v;
			arrs.push_back(v);
		}

		for (int i = 0; i < len; ++i) {
			int num = data[i] / base;
			int j;
			for (j = 0; j < arrs[num].size(); ++j) {
				if (arrs[num][j] >= data[i])
					break;
			}
			arrs[num].insert(arrs[num].begin() + j, data[i]);
		}

		vector<int> result;
		for (auto rows : arrs)
			for (auto cols : rows)
				result.push_back(cols);

		return result;
	}
private:
	vector<int> data;
	int len;
	int max_n;
	int base = 10;
};

int main() {
	//vector<int> arrs = { 6, 83, 25, 306, 13, 77, 63, 142, 61, 57, 90, 77};
	default_random_engine e;
	uniform_int_distribution<int> u(0, 1000);
	vector<int> arrs;
	for (int i = 0; i < 15; ++i)
		arrs.push_back(u(e));

	//bubblesort
	BubbleSort s1(arrs);
	vector<int> result1 = s1.sort();
	s1.print(result1, "bubblesort");

	//selectsort
	SelectionSort s2(arrs);
	vector<int> result2 = s2.sort();
	s2.print(result2, "selectsort");

	//insertionsort
	InsertionSort s3(arrs);
	vector<int> result3 = s3.sort();
	s3.print(result3, "insertionsort");

	//shellsort
	ShellSort s4(arrs);
	vector<int> result4 = s4.sort();
	s4.print(result4, "shellsort");

	//mergesort
	MergeSort s5(arrs);
	vector<int> result5 = s5.sort();
	s5.print(result5, "mergesort");

	//quicksort
	QuickSort s6(arrs);
	vector<int> result6 = s6.sort();
	s6.print(result6, "quicksort");

	//heapsort
	HeapSort s7(arrs);
	vector<int> result7 = s7.sort();
	s7.print(result7, "heapsort");

	//countingsort
	CountingSort s8(arrs);
	vector<int> result8 = s8.sort();
	s8.print(result8, "countingsort");

	//bucketsort
	BucketSort s9(arrs);
	vector<int> result9 = s9.sort();
	s9.print(result9, "buckersort");
	return 0;

	//radixsort
	RadixSort s10(arrs);
	vector<int> result10 = s10.sort();
	s10.print(result10, "radixsort");
	
	return 0;
}
