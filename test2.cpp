#include <iostream>
using namespace std;

void bubbleSort(int *arr, int length) {
    bool swapped;
    for (int i = 0; i < length - 1; i++) {
        swapped = false;
        for (int j = 0; j < length - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void displayArray(const int arr[], int len) {
    for (int i = 0; i < len; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main() {
    int data[] = {5, 1, 4, 2, 8};
    int size = sizeof(data) / sizeof(data[0]);

    cout << "Before Sorting: ";
    displayArray(data, size);

    bubbleSort(data, size);

    cout << "After Sorting: ";
    displayArray(data, size);

    return 0;
}
