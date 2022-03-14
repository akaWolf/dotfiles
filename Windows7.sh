#!/bin/sh

exec qemu-system-x86_64 \
	-cpu host,hv_relaxed,hv_spinlocks=0x1fff,hv_vapic,hv_time \
	-smp 2 \
	-enable-kvm \
	-machine type=q35,accel=kvm \
	-device intel-iommu \
	-drive file=/home/akawolf/Windows7.img,format=qcow2,if=virtio \
	-net nic,model=virtio \
	-net user,hostname=windowsvm \
	-soundhw hda \
	-m 4G \
	-monitor stdio \
	-name "Windows 7" \
        -net user,smb=/home/akawolf/shared-folders/windows \
	$@

# -net user,smb=/home/akawolf/shared-folders/windows \
# -drive file=~/Downloads/virtio-win-0.1.141.iso,media=cdrom \
# -drive file=~/Downloads/en_windows_7_enterprise_with_sp1_x64_dvd_620201.iso,media=cdrom \
# -vga qxl -spice port=5930,disable-ticketing -device virtio-serial-pci -device virtserialport,chardev=spicechannel0,name=com.redhat.spice.0 -chardev spicevmc,id=spicechannel0,name=vdagent
