#include <stdio.h>

int main()
{
	int arr[10] = { 10,2,1,3,4,9,7,5,8,6 };
	int tmp;
	for (int i = 0; i < 9; ++i)
	{
		int j = i;
		while (j >= 0 && arr[j] > arr[j + 1])
		{
			tmp = arr[j];
			arr[j] = arr[j + 1];
			arr[j + 1] = tmp;
			--j;
		}
	}
	for (int i = 0; i < 9; ++i)
	{
		printf("%d ", arr[i]);
	}

	return 0;
}