```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-policy
  namespace: your-namespace
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress



```
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-from-browser
  namespace: your-namespace
spec:
  podSelector: {}
  ingress:
  - ports:
    - port: 80  # Allow incoming traffic on port 80 (HTTP)
    - port: 443 # Allow incoming traffic on port 443 (HTTPS)
    from:
    - podSelector: {}

```

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-from-specific-namespaces
  namespace: your-namespace
spec:
  podSelector: {}
  ingress:
  - ports:
    - port: 80  # Allow incoming traffic on port 80 (HTTP)
    - port: 443 # Allow incoming traffic on port 443 (HTTPS)
    from:
    - podSelector: {}
      namespaceSelector:
        matchLabels:
          namespace-label-key: namespace-label-value
    - podSelector: {}
      namespaceSelector:
        matchLabels:
          another-namespace-label-key: another-namespace-label-value

```
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-and-egress
  namespace: your-namespace
spec:
  podSelector: {}
  ingress:
  - ports:
    - port: 80  # Allow incoming traffic on port 80 (HTTP)
    - port: 443 # Allow incoming traffic on port 443 (HTTPS)
  egress:
  - to:
    - podSelector: {}
      namespaceSelector:
        matchLabels:
          namespace-label-key: namespace-label-value
    - podSelector: {}
      namespaceSelector:
        matchLabels:
          another-namespace-label-key: another-namespace-label-value

```

```
"############################################################################
"
" ooooo        ooooo ooooo      ooo ooooo     ooo ooooooo  ooooo 
" `888'        `888' `888b.     `8' `888'     `8'  `8888    d8'  
" 888          888   8 `88b.    8   888       8     Y888..8P    
" 888          888   8   `88b.  8   888       8      `8888'     
" 888          888   8     `88b.8   888       8     .8PY888.    
" 888       o  888   8       `888   `88.    .8'    d8'  `888b   
" o888ooooood8 o888o o8o        `8     `YbodP'    o888o  o88888o

" ooooo      ooo   .oooooo.   ooo        ooooo       .o.       oooooooooo.   
" `888b.     `8'  d8P'  `Y8b  `88.       .888'      .888.      `888'   `Y8b  
" 8 `88b.    8  888      888  888b     d'888      .8"888.      888      888 
" 8   `88b.  8  888      888  8 Y88. .P  888     .8' `888.     888      888 
" 8     `88b.8  888      888  8  `888'   888    .88ooo8888.    888      888 
" 8       `888  `88b    d88'  8    Y     888   .8'     `888.   888     d88' 
" o8o        `8   `Y8bood8P'  o8o        o888o o88o     o8888o o888bood8P'   
"
"############################################################################

" Vim configuration file "
"!!! COPY THIS FILE TO YOUR HOME FOLDER !!!"

" enable mouse support "
set mouse=a

" enable syntax "
syntax on

" enable line numbers "
set number

" highlight current line "
set cursorline
:highlight Cursorline cterm=bold ctermbg=black

" enable highlight search pattern "
set hlsearch

" enable smartcase search sensitivity "
set ignorecase
set smartcase

" Indentation using spaces "
" tabstop:	width of tab character
" softtabstop:	fine tunes the amount of whitespace to be added
" shiftwidth:	determines the amount of whitespace to add in normal mode
" expandtab:	when on use space instead of tab
" textwidth:	text wrap width
" autoindent:	autoindent in new line
set tabstop	=4
set softtabstop	=4
set shiftwidth	=4
set textwidth	=79
set expandtab
set autoindent

" show the matching part of pairs [] {} and () "
set showmatch

" remove trailing whitespace from Python and Fortran files "
autocmd BufWritePre *.py :%s/\s\+$//e
autocmd BufWritePre *.f90 :%s/\s\+$//e
autocmd BufWritePre *.f95 :%s/\s\+$//e
autocmd BufWritePre *.for :%s/\s\+$//e

" enable color themes "
if !has('gui_running')
	set t_Co=256
endif
" enable true colors support "
set termguicolors
" Vim colorscheme "
colorscheme desert

"-------------------------------------------------------------"
"Bonus. " Find & Replace (if you use the ignorecase, smartcase these are mandatory) "
"            :%s/<find>/<replace>/g   "replace global (e.g. :%s/mass/grass/g)"
"            :%s/<find>/<replace>/gc  "replace global with confirmation"
"            :%s/<find>/<replace>/gi  "replace global case insensitive"
"            :%s/<find>/<replace>/gI  "replace global case sensitive"
"            :%s/<find>/<replace>/gIc "replace global case sensitive with confirmation"

"        " Vim (book)marks "
"            mn     "replace n with a word A-Z or number 0-9"
"            :'n     "go to mark n"
"            :`.     "go to the last change"
"            :marks  "show all declared marks"
"            :delm n "delete mark n"

"        " Delete range selection "
"            :<line_number>,<line_number>d "(e.g. :2,10d deletes lines 2-10)"

"        " LaTeX shortcuts "
"            nnoremap <F1> :! pdflatex %<CR><CR>
"            nnoremap <F2> :! bibtex $(echo % \| sed 's/.tex$//') & disown<CR><CR>
"            nnoremap <F3> :! evince $(echo % \| sed 's/tex$/pdf/') & disown<CR><CR>
"            nnoremap <F4> :! rm *.log *.aux *.out *.blg & disown<CR><CR>
```




```
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-configmap
data:
  my-yaml-file.yaml: |
    apiVersion: ...
    # Add more YAML configurations here
```


```

apiVersion: batch/v1
kind: Job
metadata:
  name: my-job
spec:
  template:
    spec:
      containers:
      - name: my-container
        image: your-image-name:your-tag
        command: ["/bin/bash", "-c"]
        args:
        - |
          echo "Running command 1"
          kubectl apply -f /config/my-yaml-file.yaml
          command1
          echo "Running command 2"
          command2
          # Add more commands as needed
          wait
          echo "Another command"
          # Add more commands after the wait
        - |
          echo "Yet another command"
        volumeMounts:
        - name: config-volume
          mountPath: /config
      volumes:
      - name: config-volume
        configMap:
          name: my-configmap


```














































# Gists
Sure, here's a tabular summary of the weekly balanced vegetarian diet plan for a person with 105 kg weight:

| Day        | Breakfast                                           | Lunch                                 | Afternoon Snack     | Dinner                                        |
|------------|-----------------------------------------------------|---------------------------------------|---------------------|-----------------------------------------------|
| Monday     | Masala Oats with milk, chopped apples, and a banana | Dosa with coconut chutney and sambar  | Sprouts salad       | Boiled Chana curry with brown rice            |
| Tuesday    | Bread toast with avocado spread, sliced tomatoes, and a small bowl of mixed fruit salad (apples and bananas) | Idli with tomato chutney and a side of mixed vegetable curry | A glass of milk | Vegetable stir-fry with rice          |
| Wednesday  | Banana smoothie made with milk, a handful of oats, and a small bowl of yogurt with sliced bananas and a drizzle of honey | Rice with spicy chickpea curry (Chana) and cucumber raita | A small apple | Masala Oats with mixed vegetables       |
| Thursday   | Two whole grain bread slices with peanut butter, sliced bananas, and a small bowl of cottage cheese (paneer) with sliced fruits (e.g., apples, oranges) | Brown rice with mixed vegetable curry | A boiled egg (if you consume eggs) | Dosa with tomato chutney and a side of sprouts salad |
| Friday     | Apple slices with cottage cheese (paneer) and a small bowl of Greek yogurt with chopped apples and a sprinkle of granola | Vegetable biryani with raita | A glass of milk | Boiled Chana salad with cucumber, tomatoes, and lemon dressing |
| Saturday   | Masala Oats with mixed vegetables, milk, and a small bowl of oatmeal with sliced bananas and a drizzle of honey | Rice with spicy chickpea curry (Chana) and a side of stir-fried vegetables | A small apple | Idli with coconut chutney and a side of sambar |
| Sunday     | Choose a hearty breakfast or brunch of your choice that includes a mix of whole grains, fruits, vegetables, and protein (e.g., veggie omelette, whole grain toast with avocado spread, smoothie bowl) | Rice with spicy chickpea curry (Chana) and cucumber raita | A glass of milk | Boiled Chana salad with cucumber, tomatoes, and lemon dressing |

Remember to drink plenty of water throughout the day and adjust the portion sizes based on your individual dietary needs and activity levels. Enjoy a balanced and nutritious week!
