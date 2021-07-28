#include <stdio.h>

int main()
{
	int arr[10] = { 1,10,5,8,7,6,4,3,2,9 };
	int tmp, max, index;

	for (int i = 0; i < 9; ++i)
	{
		max = 100;
		for (int j = i; j < 9; ++j)
		{
			if (max > arr[j])
			{
				max = arr[j];
				index = j;
			}
		}
		
		tmp = arr[i];
		arr[i] = arr[index];
		arr[index] = tmp;
	}

	for (int i = 0; i < 9; ++i)
	{
		printf("%d ", arr[i]);
	}
}