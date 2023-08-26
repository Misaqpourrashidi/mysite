from django.db import models


class Day(models.Model):
	day = models.CharField(max_length=100)

	def __str__(self):
		return f"{self.day}"

class Month_Name(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Year(models.Model):
	year = models.CharField(max_length=100)

	def __str__(self):
		return self.year


class January(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day}'

class February(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)


	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class March(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class April(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class May(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class June(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class July(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class August(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class September(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class October(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class November(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '

class December(models.Model):
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month_Name, on_delete=models.CASCADE, null=True)
	day = models.OneToOneField(Day, on_delete=models.CASCADE, null=True, unique=True)
	

	def __str__(self):
		return f'{self.year} | {self.month} | {self.day} '
