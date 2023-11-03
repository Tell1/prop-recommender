DIR := ./data/valuergeneral/raw/2022

unzip:
	@echo "Unzipping all .zip files in $(DIR)"
	@for zip in $(DIR)/*.zip; do \
		dirname=$${zip%.zip}; \
		echo "Unzipping $$zip to $$dirname"; \
		mkdir -p $$dirname; \
		unzip $$zip -d $$dirname; \
	done

reformat: # Command to convert .DAT into a csv
	@echo "Reformatting all .dat files in $(DIR)"
	@echo "Not inplemented yet"
	

setup: # create the directory structure for the path DIR
	@echo "Creating directory structure in $(DIR)"
	@mkdir -p $(DIR)


