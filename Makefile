all:
	make download

download: ss14pusa.csv
	@echo downloading the inputs.
	wget 'https://www.datalumos.org/datalumos/project/100486/version/V1/view?path=/datalumos/100486/fcr:versions/V1/ss14pusa.csv&type=file'
	wget 'https://www.datalumos.org/datalumos/project/100486/version/V1/view?path=/datalumos/100486/fcr:versions/V1/ss14pusb.csv&type=file'
	wget 'https://www.datalumos.org/datalumos/project/100486/version/V1/view?path=/datalumos/100486/fcr:versions/V1/ss14pusc.csv&type=file'
	wget 'https://www.datalumos.org/datalumos/project/100486/version/V1/view?path=/datalumos/100486/fcr:versions/V1/ss14pusd.csv&type=file'