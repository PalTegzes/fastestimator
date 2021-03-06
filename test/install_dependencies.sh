JENKINS_DIR=$WORKSPACE/..
PATH=$JENKINS_DIR/venv/bin:/usr/local/bin:$PATH
echo $WORKSPACE
if [ ! -d "$JENKINS_DIR/venv"  ]; then
    virtualenv -p python3.6 $JENKINS_DIR/venv
fi
. $JENKINS_DIR/venv/bin/activate

pip3 install pytest numpy nibabel pydicom tensorflow-gpu==2.0.0 twine ipython ipykernel
pip3 install -e .
