# Use Rocky Linux 9 as a base image
FROM rockylinux/rockylinux:9

# Copy the Git repository from the host to the Docker image
COPY . /ObsApp_pack

ENV NEW_IP=10.1.71.29

# Copy configuration file
RUN sed -i "s/ip_addr = .*/ip_addr = ${NEW_IP}/" /ObsApp_pack/installation/ObsApp/ObsApp.ini
RUN cp -r /ObsApp_pack/installation/ObsApp /
RUN cp -r /ObsApp_pack/installation/ObsApp /ObsApp_pack/code/

# Update the system and install the necessary packages
RUN dnf update -y && \
    dnf install -y mesa-libGL mesa-libEGL fontconfig libxkbcommon dbus-libs qt5-qtbase-gui bzip2

# Install Miniconda and Python libraries
RUN bash /ObsApp_pack/installation/Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3 && \
    /root/miniconda3/bin/conda clean -i -y && \
    ln -s /root/miniconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /root/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate" >> ~/.bashrc

ENV PATH /root/miniconda3/bin:$PATH

RUN conda update conda -y && \
    conda create -n ObsApp python=3.9 -y && \
    /root/miniconda3/envs/ObsApp/bin/pip install numpy astropy matplotlib pyside6==6.4.2 PyQt5 pika scipy

RUN strip --remove-section=.note.ABI-tag /root/miniconda3/envs/ObsApp/lib/python3.9/site-packages/PySide6/Qt/lib/libQt6Core.so.6

# Clean up
RUN dnf clean all


