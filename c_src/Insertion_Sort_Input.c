#include <stdio.h>

int main()
{
	int n, tmp;
	int arr[101];

	printf("��� ���ڸ� �����Ұ��� �Է��Ͻÿ�.\n");
	scanf_s("%d", &n);

	for (int i = 0; i < n; ++i)
	{
		if (i == 0) printf("���ڸ� �Է��Ͻÿ�.\n");
		scanf_s("%d", &arr[i]);
	}

	for (int i = 0; i < n; ++i)
	{
		int j = i;
		while (j > 0 && arr[j - 1] > arr[j])
		{
			tmp = arr[j - 1];
			arr[j - 1] = arr[j];
			arr[j] = tmp;
			--j;
		}
	}

	for (int i = 0; i < n; ++i)
	{
		printf("%d ", arr[i]);
	}

	return 0;
}