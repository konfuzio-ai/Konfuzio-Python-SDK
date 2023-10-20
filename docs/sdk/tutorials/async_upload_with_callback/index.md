.. _async_upload_with_callback:

## Pull Documents Uploaded Asynchronously with a Webhook

The most convenient way to upload a large number of files to Konfuzio is to use the `Document.from_file` method in 
asynchronous mode. That way, you can upload multiple files without having to wait for them to be processed by our 
backend. The downside of this method is that you will not know when the processing is finished and when you will be 
able to access the results. One solution to this problem is to use a [webhook callback URL](https://dev.konfuzio.com/web/api-v3.html#asynchronous-document-processing-with-webhook). 
This URL can notify your application when the processing is done. In this tutorial we will use [ngrok](https://ngrok.com/) 
to expose a local web server and create a callback URL that will receive the callback responses from the Konfuzio Server 
and then allow us to update the files with the OCR information.

### Preliminary Steps

1. **Set up Konfuzio**

    First, make sure that you have the Konfuzio SDK installed and that you have a Konfuzio account with a Project to use. 
    If you don't have this yet, please follow the instructions in the [Get Started guide](https://dev.konfuzio.com/sdk/get_started.html#get-started).

2. **Install Flask**

    Next, install Flask, which we will use to create a simple web server that will receive the callback from the Konfuzio
    Server. You can install Flask using pip:

    ```console
    pip install flask
    ```

3. **Set up ngrok**

    Then you will need to set up ngrok. If you already have a public web server able to receive post calls, you can 
    ignore this step and just use the callback URL to your web server's callback end point. To set up ngrok, first 
    create an account on the [ngrok website](https://ngrok.com/). It's free and you can use your GitHub or Google 
    account.

    Once logged into ngrok, simply follow the simple instructions available at https://dashboard.ngrok.com/get-started/setup
    On linux, all you need to do is:
    - Download ngrok
    - Follow the instructions to add the authentication token
    - Run this in a terminal:

    ```console
    ./ngrok http 5000
    ```
    This should give you the URL you can use as a callback URL. It should look something like 
    "https://abcd-12-34-56-789.ngrok-free.app".

Now that we have ngrok set up, we can see how to use it to pull the results of asynchronously uploaded files.

### Retrieving asynchronously uploaded files using a callback URL

1. **Import the necessary modules**

    ```python
    from flask import Flask, request
    from konfuzio_sdk.data import Project, Document
    import threading
    from werkzeug.serving import run_simple
    ```

2. **Create a project object**

    You will find your Project id in the Konfuzio web interface.

    ```python
    project = Project(id_=YOUR_PROJECT_ID)
    ```

3. **Create a Flask application**

    ```python
    app = Flask(__name__)
    ```

4. **Set the callback URL**

    You will find this callback url in the ngrok console where you ran `./ngrok http 5000`.

    ```python
    callback_url = YOUR_CALLBACK_URL  # It should look something like "https://abcd-12-34-56-789.ngrok-free.app"
    ```

5. **Initialize data structures to share information between the threads**

    We will use the main thread to host our Flask application and to receive the callback responses. We will use a 
    separate thread to send the files to the Konfuzio Server. So, we will use the `callback_data_dict` to store the 
    callback responses. The `data_lock` will be used to synchronize access to the `callback_data_dict` between the 
    two threads, so that we can safely access it from both threads.

    ```python
    callback_data_dict = {}

    data_lock = threading.Lock()
    ```

6. **Create a callback function**

    Now we can create the callback function that will receive the callback responses from the Konfuzio server. We simply
    store the callback response in the `callback_data_dict` and set the `callback_received` event to notify the thread
    which is sending the files that the callback response has been received and that the files can be updated with the 
    new OCR information.

    ```python
    @app.route('/', methods=['POST'])
    def callback():
        data = request.json
        file_name = data.get('data_file_name')
        with data_lock:
            if file_name is not None and file_name in callback_data_dict:
                callback_data_dict[file_name]['callback_data'] = data
                callback_data_dict[file_name]['callback_received'].set()
        return '', 200
    ```

7. **Create a function to send your files asynchronously and update them once a callback response is received**

    Now we can create the function that will send the files to the Konfuzio Server. We create a Document object for each
    file and set the `sync` parameter to `False` to indicate that we want to upload the files asynchronously. We also 
    set the `callback_url` parameter to the callback URL we created earlier.

    We then start a thread for each Document to wait for the callback response to be received. Once the callback 
    response for a Document has been received, we can update it with the OCR information.

    ```python
    def update_file(document, file_name):
        print(f'Waiting for callback for {document}')
        callback_data_dict[file_name]['callback_received'].wait()
        
        print(f'Received callback for {document}')

        # Once the callback is received we can update our Document with the OCR information    
        document.update()
        assert document.ocr_ready

        print(f'Updated {document} information with OCR results')

    def send_files(file_names):
        for file_name in file_names:
            with data_lock:
                callback_data_dict[file_name] = {'callback_received': threading.Event(), 'callback_data': None, 'document': None}
            print(f'Sending {file_name} to Konfuzio servers...')
            document = Document.from_file(file_name, project=project, sync=False, callback_url=callback_url)
            with data_lock:
                callback_data_dict[file_name]['document'] = document

        # Wait for callbacks
        for file_name in callback_data_dict:
            threading.Thread(target=update_file, args=(callback_data_dict[file_name]['document'], file_name,)).start()
    ```

8. **Start the Flask application and upload the files**

    Finally, we can start the Flask application and send the files. Simply add the path to all the files you want to
    upload. 

    ```python
    if __name__=='__main__':
        thread = threading.Thread(target=lambda: run_simple("0.0.0.0", 5000, app))
        thread.start()
        file_names = ['LIST.pdf', 'OF.jpg', 'FILES.tiff']
        threading.Thread(target=send_files, args=(file_names,)).start()
    ```
