### Review for Colleague from Platform Engineering (she/her)

1. **Contributes to overall team:**  
   She consistently contributes to the platform engineering team's success by streamlining processes, identifying gaps, and suggesting innovative approaches that enhance team efficiency. Her work is a key pillar in achieving the team's goals.

2. **Delivers solutions:**  
   She is solution-oriented, consistently delivering robust, scalable, and efficient solutions. Her technical expertise and problem-solving abilities have led to several successful deployments that have significantly improved the platform.

3. **Works collaboratively:**  
   She fosters a collaborative work environment by always being open to sharing her knowledge, engaging in cross-team discussions, and helping others troubleshoot technical challenges. Her approachable nature encourages open communication.

4. **Proactive risk mitigation:**  
   She excels at identifying potential risks in projects early on and actively works to mitigate them. Her proactive approach ensures that projects run smoothly and potential setbacks are addressed before they escalate.

5. **Acts not only within the letter but also the spirit of applicable policies:**  
   She fully understands and follows both the letter and spirit of our team’s policies, ensuring that her work aligns with the platform's objectives while maintaining compliance with relevant guidelines.

6. **Effective engagement:**  
   Her engagement in team meetings and brainstorming sessions is highly effective. She listens actively, provides thoughtful input, and helps steer conversations towards productive outcomes.

7. **Takes accountability:**  
   She takes full accountability for her work, acknowledging mistakes when they occur and working diligently to correct them. Her accountability enhances the overall integrity of the team's output.

8. **Contributes to an inclusive and diverse work environment:**  
   She actively contributes to building an inclusive and diverse environment, ensuring everyone feels heard and valued. She brings diverse perspectives to the table, which enhances the team's decision-making.

9. **Treats others with respect:**  
   She consistently treats her colleagues with the utmost respect, showing empathy, and valuing the opinions of others, even during challenging situations.

---

### Review for Colleague from Observability Team (he/him)

1. **Contributes to overall team:**  
   He plays a vital role in the observability team by designing and maintaining critical monitoring tools that support the platform's reliability and performance. His contributions directly improve the platform’s stability.

2. **Delivers solutions:**  
   He is a go-to person for delivering effective observability solutions, especially in troubleshooting complex monitoring issues. His technical acumen is reflected in the seamless operation of observability systems across the platform.

3. **Works collaboratively:**  
   He excels in cross-team collaboration, often engaging with platform engineering and other teams to ensure observability tools are well-integrated. His openness to collaboration improves overall operational insights.

4. **Proactive risk mitigation:**  
   His ability to foresee potential performance or monitoring issues before they become critical sets him apart. He is constantly refining monitoring solutions to preemptively mitigate risks.

5. **Acts not only within the letter but also the spirit of applicable policies:**  
   He understands the importance of observability not just as a technical function but as a responsibility tied to platform reliability. His adherence to both technical policies and broader organizational goals is commendable.

6. **Effective engagement:**  
   He actively engages in team discussions and technical forums, providing valuable insights on observability practices. His contributions help the team stay ahead in adopting best practices.

7. **Takes accountability:**  
   He takes ownership of his work, ensuring that observability solutions are thoroughly tested and reliable. If issues arise, he is quick to address them, ensuring minimal impact on the platform.

8. **Contributes to an inclusive and diverse work environment:**  
   He advocates for a diverse and inclusive workplace, encouraging the sharing of diverse viewpoints within his team, which contributes to more creative and comprehensive solutions.

9. **Treats others with respect:**  
   He consistently treats his colleagues with respect, whether it’s during technical debates or day-to-day interactions. He values everyone’s input, fostering a positive and professional atmosphere.

It looks like `script_a.sh` is getting stuck at `script_b.sh &`, which is intended to run in the background, but something in `script_b.sh` might still be causing the blocking behavior.

Here are a few things to check and try to resolve the issue:

### 1. **Redirect Output of `script_b.sh`:**
   The issue might be caused by `script_b.sh` still writing to standard output or standard error. By default, even when run in the background, the script's output may still tie up the terminal and prevent `script_a.sh` from continuing.

   Try redirecting both `stdout` and `stderr` to `/dev/null` to fully detach the background process:

   ```bash
   script_b.sh > /dev/null 2>&1 &
   ```

### 2. **Disown the Background Process:**
   After putting the process in the background, you may want to disown it so that it doesn't hold up the parent process (`script_a.sh`).

   ```bash
   script_b.sh > /dev/null 2>&1 &
   disown
   ```

   `disown` ensures that `script_a.sh` won't wait on `script_b.sh` to complete or interact with it.

### 3. **Check `script_b.sh` Logic:**
   Ensure that `script_b.sh`'s loop or any code within isn't hanging or misbehaving in such a way that it's affecting the parent script. If `script_b.sh` takes too long to initialize, it might also give the impression that `script_a.sh` is stuck.

### Example `script_a.sh`:

```bash
# code here 1...

# Run script_b.sh in background, with output and error redirected and process disowned
script_b.sh > /dev/null 2>&1 &

disown

# code here 2 ...
```

### Example `script_b.sh`:

```bash
while true
do
    # Some background task
    echo "Background process running"
    
    sleep 5
done
```

This approach should allow `script_a.sh` to continue after starting `script_b.sh` in the background without being blocked.
```

```
import subprocess
import json
import pandas as pd
from datetime import datetime, timezone

def get_pods_dataframe(namespace='default'):
    # Execute the kubectl command and capture the output in JSON format
    result = subprocess.run(['kubectl', 'get', 'pods', '-n', namespace, '-o', 'json'], stdout=subprocess.PIPE)
    pods_json = json.loads(result.stdout.decode('utf-8'))
    
    # Extract relevant data for the DataFrame
    pods_data = []
    for item in pods_json['items']:
        # Extract the required fields
        name = item['metadata']['name']
        ready = f"{sum(1 for cs in item['status']['containerStatuses'] if cs['ready'])}/{len(item['status']['containerStatuses'])}"
        status = item['status']['phase']
        restarts = sum(cs['restartCount'] for cs in item['status']['containerStatuses'])
        start_time = item['status'].get('startTime')
        
        # Calculate age in a human-readable format
        if start_time:
            start_time_dt = datetime.fromisoformat(start_time.rstrip('Z')).replace(tzinfo=timezone.utc)
            age = datetime.now(timezone.utc) - start_time_dt
            age_str = str(age).split('.')[0]  # Remove microseconds
        else:
            age_str = 'N/A'
        
        pods_data.append({
            'name': name,
            'ready': ready,
            'status': status,
            'restarts': restarts,
            'age': age_str
        })
    
    # Create and return the DataFrame
    return pd.DataFrame(pods_data)

# Example usage
df = get_pods_dataframe('default')
print(df)


```
```
import time

class Timer:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(f"Time taken: {self.elapsed_time} seconds")

# Using the context manager
with Timer():
    # This is the code block whose execution time is being measured
    for i in range(1000000):
        pass  # Replace with your actual code

```


```
#!/bin/bash

# Get the pod information in a raw format
pods_info=$(kubectl get pods -n default --no-headers)

# Initialize an empty JSON object
json_result='{ "result": ['

# Iterate over each line of the pod information
while IFS= read -r line; do
  # Extract the required fields using awk
  pod_name=$(echo $line | awk '{print $1}')
  ready=$(echo $line | awk '{print $2}')
  status=$(echo $line | awk '{print $3}')
  restarts=$(echo $line | awk '{print $4}')
  age=$(echo $line | awk '{print $5}')

  # Append to the JSON object
  json_result+='
    {
      "name": "'$pod_name'",
      "ready": "'$ready'",
      "status": "'$status'",
      "restarts": "'$restarts'",
      "age": "'$age'"
    },'
done <<< "$pods_info"

# Remove the trailing comma and close the JSON array
json_result=$(echo $json_result | sed 's/,$//')
json_result+=' ]}'

# Print the JSON object
echo "$json_result" | jq .

```

Creating a structured Flask API with the specified folder structure involves organizing your code in a modular way, making it easier to manage and maintain. Here’s a step-by-step guide with the example code for each file:

### Folder Structure
```
my_flask_app/
├── app.py
├── routes/
│   ├── __init__.py
│   ├── flux.py
│   ├── kube_ctl.py
│   └── helmctl.py
└── utils/
    ├── __init__.py
    └── util.py
```

### 1. app.py
This is the main file that initializes the Flask application and registers the blueprints.

```python
from flask import Flask
from routes.flux import flux_bp
from routes.kube_ctl import kube_ctl_bp
from routes.helmctl import helmctl_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(flux_bp, url_prefix='/flux')
app.register_blueprint(kube_ctl_bp, url_prefix='/kube')
app.register_blueprint(helmctl_bp, url_prefix='/helm')

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. routes/flux.py
This file defines the routes related to Flux.

```python
from flask import Blueprint, jsonify

flux_bp = Blueprint('flux', __name__)

@flux_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Flux is running"})
```

### 3. routes/kube_ctl.py
This file defines the routes related to Kubernetes control.

```python
from flask import Blueprint, jsonify

kube_ctl_bp = Blueprint('kube_ctl', __name__)

@kube_ctl_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Kubernetes control is running"})
```

### 4. routes/helmctl.py
This file defines the routes related to Helm control.

```python
from flask import Blueprint, jsonify

helmctl_bp = Blueprint('helmctl', __name__)

@helmctl_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Helm control is running"})
```

### 5. utils/util.py
This file contains utility functions that can be used across different parts of the application.

```python
def common_util_function():
    return "This is a common utility function."
```

### 6. routes/__init__.py
This file makes the `routes` directory a package.

```python
# This file can be empty or you can initialize something if needed.
```

### 7. utils/__init__.py
This file makes the `utils` directory a package.

```python
# This file can be empty or you can initialize something if needed.
```

### Putting It All Together
1. **Run the Application**: To run the application, navigate to the directory containing `app.py` and execute the command:
    ```bash
    python app.py
    ```
2. **Access the Endpoints**:
    - Flux status: `http://127.0.0.1:5000/flux/status`
    - Kubernetes control status: `http://127.0.0.1:5000/kube/status`
    - Helm control status: `http://127.0.0.1:5000/helm/status`

This structure organizes the code into separate files for different routes and utilities, making it modular and easier to manage.


<br/>
<br/>
<br/>
<br/>


```
When Gremlin is installed into an SELinux system as a container (e.g Docker constainer, Kubernetes daemonset), the container runtime that manages Gremlin will run the Gremlin processes under the SELinux process label type container_t. Gremlin performs some actions that are not allowed by this process label:

    Install and manipulate files on the host: /var/lib/gremlin, /var/log/gremlin
    Load kernel modules for manipulating network transactions during network attacks, such as net_sch
    Communicate with the container runtime socket (e.g. /var/run/docker.sock) to launch containers that carry out attacks
    Read files in /proc

When you install Gremlin as root directly onto your host machines, you likely do not need to install any of these policies, as Gremlin should run under SELinux process label type unconfined_t.

To alleviate the privilege restrictions imposed on container_t, you can allow these privileges to container_t, providing Gremlin with everything it needs, but this would also give the same privileges to all other containers on your system, which is not ideal.

This project crates a new process label type gremlin.process and adds all the necessary privileges Gremlin needs, so that you can grant them to Gremlin only, and nothing else.

Gremlin builds on the SELinux inheritance patterns set out in containers/udica, providing Gremlin privileges on top of standard container privileges. See the policy here.

https://github.com/gremlin/selinux-policies
```


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
