#include <stdio.h>

int main()
{
	
	int arr[10] = { 1,10,5,8,7,6,4,3,2,9 };
	int tmp;

	for (int i = 0; i < 9; ++i)
	{
		for (int j = i; j < 9; ++j)
		{
			if (arr[i] > arr[j])
			{
				tmp = arr[i];
				arr[i] = arr[j];
				arr[j] = tmp;
			}
		}
	}

	for (int i = 0; i < 9; ++i)
	{
		printf("%d  ", arr[i]);
	}

	return 0;
}