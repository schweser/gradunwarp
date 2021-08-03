docker run --rm repronim/neurodocker:0.7.0 generate docker \
    --pkg-manager apt \
    --base ubuntu:16.04 \
    --fsl version=6.0.3 \
    --freesurfer version=6.0.1 \
> fsl603_freesurfer601.Dockerfile

docker build --tag fsl603_freesurfer601 --file fsl603_freesurfer601.Dockerfile .
