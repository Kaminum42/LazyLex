#include <bits/stdc++.h>
using namespace std;

const int maxn = 1e5 + 53;

int a[maxn];

inline int ra(int n) { // [0, n)
	return (((rand() * RAND_MAX + rand()) % n) + n) % n;
}

inline int ra(int l, int r) { // [l, r)
	return ra(r - l) + l;
}

void quicksort(int *arr, int l, int r) {
	if(r - l <= 1)
		return;
	swap(arr[l], arr[ra(l, r)]);
	int p = arr[l], i = l, j = l + 1, k = r;
	while(j < k) {
		if(arr[j] < p)
			swap(arr[i], arr[j]), ++i, ++j;
		else if(arr[j] > p)
			swap(arr[j], arr[k - 1]), --k;
		else
			++j;
	}
	quicksort(arr, l, i);
	quicksort(arr, k, r);
}

int main() {
    /* A real quicksort example program. */
	srand(unsigned(time(NULL)));
	int n;
	cin >> n;
	for(int i = 1; i <= n; ++i)
		cin >> a[i];
	quicksort(a, 1, n + 1);
	for(int i = 1; i <= n - 1; ++i)
		cout << a[i] << ' ';
	cout << a[n] << endl;
    return 0;
}