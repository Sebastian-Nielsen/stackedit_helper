from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import re, os, clipboard, pickle
from FileStructure import *
from typing import List


"""READ-ME.md


## Option-comments
Comments that aren't visible previewing the md. They are placed at the beginning of each file 
denoting the options for the file's upstream to GitHub.    
```
[template]: <> (CUSTOM - default INDEX.txt)
```


"""

############################ ALTER THESE VARIABLES FOR YOUR ENVIRONMENT ###########################
DEBUG = True
FULL_PATH_TO_CHROMDRIVER_EXE = "C:/Users/sebas/OneDrive/Dokumenter/chromedriver.exe"
REPO_URL_FOR_GITHUB_UPSTREAM = "https://github.com/sebastian-nielsen/sebastian-nielsen.github.io"
DEFAULT_TEMPLATE_INDEX_PAGE = 'CUSTOM - default index.txt'
DEFAULT_TEMPLATE_PAGE       = 'CUSTOM - default page.txt'
###################################################################################################

class ChromeBrowser(webdriver.Chrome):
	def __init__(self, path_to_chromedriver_exe):
		super().__init__(path_to_chromedriver_exe)
		self.maximize_window()

	def setZoom(self, value: int):
		"""
		Side-effect: reloads current page
		WARNING!: Clicking on elements doesn't work when zoom-value is not 1
		"""
		url = self.current_url
		self.get('chrome://settings/')
		self.execute_script(f"chrome.settingsPrivate.setDefaultZoom({value});")
		self.get(url)


class StackEdit:
	#### Click on a menu-buttons ########################################################
	def clickPublishInMenu(self, DEBUG=True):  # Click on `publish` button in menu
		el = browser.find_element_by_css_selector("body > div.app.app--light > div.layout > div > div.layout__panel.layout__panel--side-bar > div > div.side-bar__inner > div.side-bar__panel.side-bar__panel--menu > a:nth-child(6)")
		self.clickWithSeveralAttempts(el, sleepTimeSec=0.1, maxAttempts=100, DEBUG_NAME="publish-but in menu")
	#####################################################################################

	def addGithubAccount(self):
		self.clickPublishInMenu()
		# Click on `Add Github Account` button
		button = WebDriverWait(browser, 10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.app.app--light > div.layout > div > div.layout__panel.layout__panel--side-bar > div > div.side-bar__inner > div.side-bar__panel.side-bar__panel--menu > div > a:nth-child(6)")))
		button.click()
		# Click `Grant access to private repositories`
		browser.find_element_by_css_selector("body > div.app.app--light > div.modal > div.modal__inner-1 > div > div.modal__content > div.form-entry > div > label > input[type=checkbox]").click()
		# Click `OK`
		browser.find_element_by_css_selector("body > div.app.app--light > div.modal > div.modal__inner-1 > div > div.modal__button-bar > button.button.button--resolve").click()
		# Switch browser focus to the newly opened tab
		browser.switch_to.window(browser.window_handles[-1])
		# Write the github username/password to inputfields
		browser.find_element_by_id("login_field").send_keys("Sebastian-Nielsen")
		browser.find_element_by_id("password").send_keys("21Seba5938Syh47nbj")
		# Click `Sign in`
		browser.find_element_by_css_selector("#login > form > div.auth-form-body.mt-3 > input.btn.btn-primary.btn-block").click()
		# Switch browser focus back to main StackEdit tab
		browser.switch_to.window(browser.window_handles[0])
		# Go back to menu
		browser.find_element_by_css_selector(
			"body > div.app.app--light > div.layout > div > div.layout__panel.layout__panel--side-bar > div > div.side-title.flex.flex--row > button:nth-child(1)").click()

	def loadStackEdit(self, DEBUG=True):
		"""
		1. Loads the webpage
		2. Opens all side menus and closes pop-ups
		"""
		if DEBUG: print("loadStackEdit()    Starting")
		# Load site
		browser.get('https://stackedit.io/app#')
				# Wait for site to load
		# CLose popup
		WebDriverWait(browser, 10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR,
			                                "body > div.app.app--light > div.layout > div.tour > div > div > div > button:nth-child(1)"))).click()
		# Open right-side menu
		browser.find_element_by_css_selector("body > div.app.app--light > div.layout > div.layout__panel.flex.flex--row > div.layout__panel.flex.flex--column > div.layout__panel.layout__panel--navigation-bar > nav > div.navigation-bar__inner.navigation-bar__inner--right.navigation-bar__inner--button > button").click()
		# Open left-side menu
		browser.find_element_by_css_selector("body > div.app.app--light > div.layout > div > div.layout__panel.flex.flex--column > div.layout__panel.layout__panel--navigation-bar > nav > div.navigation-bar__inner.navigation-bar__inner--left.navigation-bar__inner--button > button").click()
		if DEBUG: print("loadStackEdit()    Ending")

	def importWorkspace(self):
		if DEBUG: print('ImportWorkspace()   Starting')
		# Click on `Workspace backups`

		el = self.findElement_serveralAttempts(
			method=browser.find_element_by_css_selector,
			methodInput_str="body > div.app.app--light > div.layout > div > div.layout__panel.layout__panel--side-bar > div > div.side-bar__inner > div.side-bar__panel.side-bar__panel--menu > a:nth-child(21)",
			maxAttempts=99999,
			sleepTimeSec=1
		)
		self.clickWithSeveralAttempts(el, maxAttempts=99999, sleepTimeSec=0.1)

		# Scroll `Import backups` button into view    EDIT: NOT NEEDED
		# scrollableEL = browser.find_element_by_css_selector("body > div.app.app--light > div.layout > div > div.layout__panel.layout__panel--side-bar > div > div.side-bar__inner")
		# scrollableEL.location_once_scrolled_into_view
		# browser.execute_script("arguments[0].scrollIntoView();", element)

		# Click on `Import backups`
		fileToUpload = os.path.abspath('StackEdit workspace.json')
		inputEl = browser.find_element_by_id("import-backup-file-input")
		# Upload the newset backup workspace
		inputEl.send_keys(fileToUpload)
		# Prepare newly imported backup-workspace
		self.prepareImportedWorkspace()
		# Leave the `workspace backups` section
		browser.find_element_by_css_selector("body > div.app.app--light > div.layout > div > div.layout__panel.layout__panel--side-bar > div > div.side-title.flex.flex--row > button:nth-child(1)").click()
		if DEBUG: print('clickOnImportWorkspace()   Ending')

	def prepareImportedWorkspace(self):
		# Delete welcome file
		elToDelete = browser.find_element_by_css_selector("body > div.app.app--light > div.layout > div > div.layout__panel.layout__panel--explorer > div > div.explorer__tree > div > div.explorer-node__children > div:nth-last-child(2)")
		assert elToDelete is not None
		self.deleteWebdriverElement(elToDelete)

	def deleteWebdriverElement(self, element):
		browser.execute_script("""
		var element = arguments[0];
		element.parentNode.removeChild(element);
		""", element) # Note: The element passed to `execute_script` appears as `arguments` [type list]

	def getCollapsedFolderEls(self) -> []:
		# An unfiltered list of "folder elements"
		# that are not already "expanded/opened"
		unfilteredCollapsedFolderEls_list = browser.find_elements_by_css_selector('.explorer-node--folder.explorer-node:not(.explorer-node--open')

		# Filter away elements that are not dummies or "default ones" like the 'Trash' or 'temp' folder.
		CollapsedFolderEls_list = [el for el in unfilteredCollapsedFolderEls_list     # Note:  `el.text` is the folderName
		                         if not (el.text == '' or el.text == 'Trash' or el.text == 'Temp')
		                         ]
		return CollapsedFolderEls_list

	def getNonfolderEls(self) -> []:
		"""
		Filters apart folders named the empty-string,
		as those obviously aren't real folders.
		"""
		# list of non-folder els
		nonfolderEls = browser.find_elements_by_css_selector(
			'.explorer-node:not(.explorer-node--folder')
		return list(filter(lambda el: el.text, nonfolderEls))

	def republishAllFiles(self) -> None:
		# TODO: Refactor this function
		for el in self.getNonfolderEls():
			el.click()
			retry_count = 0
			while retry_count < 15:
				try:
					# Click on the republish button
					browser.find_element_by_css_selector("body > div.app.app--light > div.layout > div > div.layout__panel.flex.flex--column > div.layout__panel.layout__panel--navigation-bar > nav > div.navigation-bar__inner.navigation-bar__inner--right.navigation-bar__inner--title.flex.flex--row > div.flex.flex--row > button.navigation-bar__button.navigation-bar__button--publish.button").click()
					break
				except:
					# Not click-able yet
					sleep(0.5)
					retry_count += 1

			retry_count = 0

	def addDefaultOptionCommentsToAllFiles(self) -> None:
		# TODO: NOT YET FULLY IMPLEMENTED YET! DONT USE THIS FUNCTION
		"""
		Side effect: Adds the default option-comment to each file. Default option comments:
		```
		[template]: <> (CUSTOM - default index.txt)
		```
		"""
		for el in self.getNonfolderEls():
			el.click()
			sleep(0.05) # Wait for editor to load

			# Place cursor in the start of the editor textfield
			findElement_serveralAttempts(method=browser.find_element_by_css_selector,
			                             methodInput_str="body > div.app.app--light > div.layout > div > div.layout__panel.flex.flex--column > div.layout__panel.flex.flex--row > div.layout__panel.layout__panel--editor > div.editor > pre",
			                             maxAttempts=2000, sleepTimeSec=0.001)
			x_body_offset = editorEl.location['x']
			y_body_offset = editorEl.location['y']
			actions = ActionChains(browser)
			actions.move_to_element_with_offset(editorEl, -x_body_offset, -y_body_offset)
			actions.move_by_offset( x, y ).click().perform()

			# Find all optionComments in the editor;
			unparsedOptions = [el.text
			                   for el in browser.find_elements_by_css_selector(".token.linkdef")]
			# Parse the optionComments
			parsedOptions = parseOptions(unparsedOptions)

			try:
				parsedOptions['file-path']
			except KeyError:
				# Determine dir
				...

			editorEl.click()
			editorEl.send_keys(Keys.UP)

	def clickWithSeveralAttempts(self, element, maxAttempts=20, sleepTimeSec=0.5, DEBUG_NAME=""):
		"""Attempts to click {element} {maxAttempts} ammount of times."""
		if DEBUG_NAME: print(f"clickWithSeveralAttempts('{DEBUG_NAME}', max={maxAttempts}), sleepTimeSec={sleepTimeSec}")
		attempts = 0
		while attempts < maxAttempts:
			try:
				element.click()
				return
			except:
				print(".", end="")
				attempts += 1
				sleep(sleepTimeSec)
		raise f"clickWithSeveralAttempts(\n" \
		      f"el='{element}',\n" \
		      f"maxAttempts='{maxAttempts}',\n" \
		      f"sleepTimeSec{sleepTime}\n)"

	def findElement_serveralAttempts(self, method,
	                                 methodInput_str,
	                                 maxAttempts=9999, sleepTimeSec=0.1, DEBUG_NAME=""):
		"""
		:param method: A WebDriver method (e.g. WebDriver.find_element_by_id )
		:param methodInput_str: Inputstring to the method (e.g. "#id-test" )
		:param maxAttempts: Max attempts to try and run the method with the inputstring
		:param sleepTime: time to sleep between each attempt
		:param DEBUG_NAME: A string that describes what is being located
		:return: element if element is found, else an error is raised
		"""
		if DEBUG_NAME: print(f"findElement_serveralAttempts(DEBUG_NAME='{DEBUG_name}',\n"
		                     f"methodInput_str={methodInput_str},\n"
		                     f"maxAttempts={maxAttempts}, sleepTimeSec{sleepTime})\n")
		attempts = 0
		while attempts < maxAttempts:
			try:
				return method(methodInput_str)
			except NoSuchElementException:
				attempts += 1
				sleep(sleepTime)

		raise NoSuchElementException


	def setGithubUpstreamForAllFiles(self, DEBUG=True):
		"""
		(1) Go through each nonfolder el (file), for each one:
			(1.1) Parse the files' option-comments
			(1.2) setGithubUpstreamForFile(parsedOptions)
		:return:
		"""
		nonfolderEls = self.getNonfolderEls()
		for el in nonfolderEls:
			node = fileStructure.getNodeByTitle(el.text)
			self.clickWithSeveralAttempts(el)
			# Wait for editor content to load
			sleep(0.2)
			# editorTextfield = browser.find_element_by_css_selector("body > div.app.app--light > div.layout > div > div.layout__panel.flex.flex--column > div.layout__panel.flex.flex--row > div.layout__panel.layout__panel--editor > div.editor")
			# Find all "hidden-comments" in the editor;
			# these determine the github upstream options for the file
			unparsedOptions = [el.text
			                   for el in browser.find_elements_by_css_selector(".token.linkdef")]
			parsedOptions = self.parseOptions(unparsedOptions, node)
			if DEBUG: print(parsedOptions)
			self.setGithubUpstreamForFile(parsedOptions)

	def setGithubUpstreamForFile(self, parsedOptions: {str: str}) -> None:
		"""
		:parsedOptions: A dictionary containing the options specified
		- You have to had added a GitHub account prior to running this function
		(1) Click on `publish` in menu
		(2) Click on `Publish to GitHub`
		(3) Fill out textfields with info from options [str]
		(4) Click OK and go back to menu page
		 """
		self.clickPublishInMenu()
		# (2) Click on `Publish to GitHub`
		browser.find_element_by_xpath(f"//*[contains(text(), 'Publish to GitHub')]").click()
		sleep(0.05)

		# (3) Fill out textfields with info from options
		filepathTextfield = self.findElement_serveralAttempts(
			method = browser.find_element_by_css_selector,
			methodInput_str = "body > div.app.app--light > div.modal > div.modal__inner-1 > div > div.modal__content > div:nth-child(4) > div.form-entry__field > input",
			maxAttempts = 1000,
			sleepTimeSec = 0.001
		)
		filepathTextfield.send_keys(Keys.CONTROL, 'a')
		filepathTextfield.send_keys(Keys.DELETE)
		try:
			filepathTextfield.send_keys(parsedOptions['file-path'])
		except KeyError:
			return
		# # Repo URL
		repo_URL = browser.find_element_by_css_selector("body > div.app.app--light > div.modal > div.modal__inner-1 > div > div.modal__content > div:nth-child(3) > div.form-entry__field > input")
		repo_URL.send_keys(REPO_URL_FOR_GITHUB_UPSTREAM)
		# # Choose template from dropdown
		select_el = browser.find_element_by_css_selector("body > div.app.app--light > div.modal > div.modal__inner-1 > div > div.modal__content > div:nth-child(6) > div.form-entry__field > select")
		select_instance = Select(select_el)
		select_instance.select_by_visible_text(parsedOptions['template'])

		# (4)
		# Click OK
		browser.find_element_by_css_selector("body > div.app.app--light > div.modal > div.modal__inner-1 > div > div.modal__button-bar > button.button.button--resolve").click()
		# Go back to menu page
		browser.find_element_by_css_selector("body > div.app.app--light > div.layout > div > div.layout__panel.layout__panel--side-bar > div > div.side-title.flex.flex--row > button:nth-child(1)").click()


	def parseOptions(self, options: [str], node: Node) -> {str: str}:
		"""Parse the options
			from

					[template]: <> (CUSTOM - default page)

			to

		{
			'template': 'CUSTOM - default page'
		}
		"""
		rtrn_dict = {
			"template": DEFAULT_TEMPLATE_INDEX_PAGE if (node.title == "index")
									else DEFAULT_TEMPLATE_PAGE,

										# Throw away 'Personal website' in the generatedPathToNode
			"file-path": fileStructure.generatePathToNode(node).split('/',1)[1] + ".html"
		}
		# for unparsedComment_str in options:
		# 	for option in ("template"):
		# 		#	# Handle general cases # #
		# 		# If the given option is what is specified in the "option-comment"
		# 		if re.search(f"^\s*\[{option}\]", unparsedComment_str):
		# 			# Then retrieve the information and store it in the rtrn_dict
		# 			# with the corresponding `option`
		# 			rtrn_dict[option] = re.search(r".*\((.*)\)\s*$", unparsedComment_str).group(1)

		return rtrn_dict

	def expandAllFolders(self, initialCall=True) -> {}:
		"""
		side-effect: Stores the fileStructure as it expands the folders
		"""
		collapsedFolderEls = self.getCollapsedFolderEls()

		# If there is a root folder
		if collapsedFolderEls and initialCall:
			el = collapsedFolderEls[0]
			fileStructure.addNode(Node(title=el.text))

		if DEBUG: print(f"------------\ncollapsedFolderEls: "
		                f"{[el.text for el in collapsedFolderEls]}")
		for el in collapsedFolderEls:
			self.clickWithSeveralAttempts(el, sleepTimeSec=0.01, maxAttempts=200)
			sleep(0.1) # wait for elements to expand
			# parent and children titles
			try:
				(parent, children) = el.text.split('\n', 1)
			except ValueError: # Folder has no children
				continue
			# Create children nodes that can be of either type: 'folder' or 'file'
			children = [Node(childTitle) for childTitle in children.split('\n')]
			fileStructure.addChildrenToNode(parent, children)

			print(f"parent:   {parent}")
			print(f"children: {children}")


		if DEBUG: print('------------')

		return self.expandAllFolders(initialCall=False) if collapsedFolderEls else None

	# def setGithubUpstreamForAllFiles():


	# def retrieveAllNonFolderElements() -> List:
	# 	# Retrieve an unfiltered list of "non-folder elements"
	# 	unfilteredNonFolderEl_list = browser.find_elements_by_css_selector('.explorer-node:not(.explorer-node--folder')
	# 	a = unfilteredNonFolderEl_list.copy()
	# 	# Filter away elements dummy elements
	# 	filteredNonFolderEl_list = [el for el in unfilteredNonFolderEl_list     # Note:  `el.text` is the folderName
	# 	                         if not (el.text == '')
	# 	                         ]
	# 	return filteredNonFolderEl_list

	def uploadTemplates(self):
		# Click on `templates` button
		el = self.findElement_serveralAttempts(
			method=browser.find_element_by_css_selector,
			methodInput_str="body > div.app.app--light > div.layout > div > div.layout__panel.layout__panel--side-bar > div > div.side-bar__inner > div.side-bar__panel.side-bar__panel--menu > a:nth-child(18)",
		)
		self.clickWithSeveralAttempts(el, maxAttempts=1000, sleepTimeSec=0.05)

		# Remove `sponser-us` banner
		sponsorBannerEl = browser.find_element_by_css_selector("body > div.app.app--light > div.modal > div.modal__sponsor-banner")
		self.deleteWebdriverElement(sponsorBannerEl)

		for templateFilename in os.listdir('Templates'):
			with open(os.path.abspath("Templates") + f"\\\\{templateFilename}", 'r', encoding="utf-8") as f:
				if DEBUG: print(f"-----\nCreating template: `{templateFilename}`")
				# Click on `New template` button
				browser.find_element_by_css_selector(
					"body > div.app.app--light > div.modal > div.modal__inner-1.modal__inner-1--templates > div > div.modal__content > div:nth-child(1) > div.form-entry__actions.flex.flex--row.flex--end > button:nth-child(1)").click()
				sleep(0.5)
				actions = ActionChains(browser)
				actions.send_keys(templateFilename)
				actions.perform()

				# Delete all content of text-field
				innerWritingField = a = browser.find_element_by_css_selector("body > div.app.app--light > div.modal > div.modal__inner-1.modal__inner-1--templates > div > div.modal__content > div:nth-child(2) > div > pre > div.cledit-section")
				browser.execute_script("arguments[0].innerHTML = ''", innerWritingField)

				# Click on the `writing` field
				writingField = browser.find_element_by_css_selector("body > div.app.app--light > div.modal > div.modal__inner-1.modal__inner-1--templates > div > div.modal__content > div:nth-child(2) > div > pre > div.cledit-section")
				self.clickWithSeveralAttempts(writingField, maxAttempts=500, sleepTimeSec=0.01)

				# Write the templateContent to it
				templateContent: str = f.read()
				clipboard.copy(templateContent)
				writingField.send_keys(Keys.CONTROL, 'v')

		# Close the `template`-popup by clicking `ok` button
		browser.find_element_by_css_selector("body > div.app.app--light > div.modal > div.modal__inner-1.modal__inner-1--templates > div > div.modal__button-bar > button.button.button--resolve").click()

if __name__ == '__main__':
	fileStructure = FileStructure()

	browser = ChromeBrowser(FULL_PATH_TO_CHROMDRIVER_EXE)
	s = StackEdit()
	s.loadStackEdit()
	s.importWorkspace() # This should be first ... always
	s.uploadTemplates()
	s.addGithubAccount()
	s.expandAllFolders()
	s.setGithubUpstreamForAllFiles()
	# retrieveAllNonFolderE lements()

	s.republishAllFiles()

1
