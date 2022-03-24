1. create a CRD

```
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.rozycki.co.uk
spec:
  group: rozycki.co.uk
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
```

2. create custom object from CRD, with finalizer for deleting finalizer

```
apiVersion: "rozycki.co.uk/v1"
kind: CronTab
metadata:
  name: my-cron-object
  finalizers:
  - deletepod.rozycki.co.uk
spec:
  cronSpec: "* * * * /5"
  image: my-cron-object
```

3. create finalizer that deletes pod(s)

TAKEN FROM https://book.kubebuilder.io/reference/using-finalizers.html

MY CHANGES HIGHLIGHTED WITH `// ***AR***`

```
func (r *CronJobReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := r.Log.WithValues("cronjob", req.NamespacedName)

    var cronJob *batchv1.CronJob
    if err := r.Get(ctx, req.NamespacedName, cronJob); err != nil {
        log.Error(err, "unable to fetch CronJob")
        // we'll ignore not-found errors, since they can't be fixed by an immediate
        // requeue (we'll need to wait for a new notification), and we can get them
        // on deleted requests.
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // name of our custom finalizer
    myFinalizerName := "deletepod.rozycki.co.uk" // ***AR***

    // examine DeletionTimestamp to determine if object is under deletion
    if cronJob.ObjectMeta.DeletionTimestamp.IsZero() {
        // The object is not being deleted, so if it does not have our finalizer,
        // then lets add the finalizer and update the object. This is equivalent
        // registering our finalizer.
        if !controllerutil.ContainsFinalizer(cronJob, myFinalizerName) {
            controllerutil.AddFinalizer(cronJob, myFinalizerName)
            if err := r.Update(ctx, cronJob); err != nil {
                return ctrl.Result{}, err
            }
        }
    } else {
        // The object is being deleted
        if controllerutil.ContainsFinalizer(cronJob, myFinalizerName) {
            // our finalizer is present, so lets handle any external dependency
            if err := r.deleteExternalResources(cronJob); err != nil {
                // if fail to delete the external dependency here, return with error
                // so that it can be retried
                return ctrl.Result{}, err
            }

	        // ***AR*** delete pods
            err:=r.DeletePods(controllerutil.kubeclient, controllerutil.podLabel)
            if err!=nil{
                fmt.Println("Failed to remove all pods. Reason: ",err)
                return nil
            }

            // remove our finalizer from the list and update it.
            controllerutil.RemoveFinalizer(cronJob, myFinalizerName)
            if err := r.Update(ctx, cronJob); err != nil {
                return ctrl.Result{}, err
            }
        }

        // Stop reconciliation as the item is being deleted
        return ctrl.Result{}, nil
    }

    // Your reconcile logic

    return ctrl.Result{}, nil
}


// ***AR*** taken from https://github.com/hossainemruz/k8s-initializer-finalizer-practice/blob/a63a7a543c747df3f37399876780cdf4f74a7d42/pkg/util/finalize.go#L9

func (r *CronJobReconciler) DeletePods(kubeclient kubernetes.Clientset,podLabel string) error {
	podClient:= kubeclient.CoreV1().Pods(api_v1.NamespaceDefault)

	podList,err:=kubeclient.CoreV1().Pods(api_v1.NamespaceDefault).List(meta_v1.ListOptions{LabelSelector: podLabel})
	if err!=nil{
		return err
	}

	for _,pod:=range podList.Items{

		delErr:=podClient.Delete(pod.GetName(),&meta_v1.DeleteOptions{})

		if delErr!=nil{
			err=delErr
		}
	}

	return err
}

func (r *Reconciler) deleteExternalResources(cronJob *batch.CronJob) error {
    //
    // delete any external resources associated with the cronJob
    //
    // Ensure that delete implementation is idempotent and safe to invoke
    // multiple times for same object.
}
```
