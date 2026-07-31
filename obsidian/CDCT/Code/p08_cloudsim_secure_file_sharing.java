import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.LinkedList;
import java.util.List;

import org.cloudbus.cloudsim.Cloudlet;
import org.cloudbus.cloudsim.CloudletSchedulerTimeShared;
import org.cloudbus.cloudsim.Datacenter;
import org.cloudbus.cloudsim.DatacenterBroker;
import org.cloudbus.cloudsim.DatacenterCharacteristics;
import org.cloudbus.cloudsim.Host;
import org.cloudbus.cloudsim.Log;
import org.cloudbus.cloudsim.Pe;
import org.cloudbus.cloudsim.Storage;
import org.cloudbus.cloudsim.UtilizationModel;
import org.cloudbus.cloudsim.UtilizationModelFull;
import org.cloudbus.cloudsim.Vm;
import org.cloudbus.cloudsim.VmAllocationPolicySimple;
import org.cloudbus.cloudsim.VmSchedulerTimeShared;
import org.cloudbus.cloudsim.core.CloudSim;
import org.cloudbus.cloudsim.provisioners.BwProvisionerSimple;
import org.cloudbus.cloudsim.provisioners.PeProvisionerSimple;
import org.cloudbus.cloudsim.provisioners.RamProvisionerSimple;

/**
 * P08 - Simulate a "secure file sharing" workflow using CloudSim.
 *
 * A user wants to share a confidential file with another user in the cloud.
 * The sharing workflow is split into compute tasks (cloudlets):
 *   1. encrypt   - AES-encrypt the file (compute bound)
 *   2. upload    - push ciphertext to cloud storage (network bound)
 *   3. download  - recipient pulls the ciphertext (network bound)
 *   4. decrypt   - AES-decrypt the file (compute bound)
 *   5. audit     - write an access-audit record (light task)
 *
 * CloudSim simulates the VM/datacenter resource usage and scheduling of
 * these tasks; it does NOT simulate cryptography itself. The security
 * aspects (AES keys, signatures, access control) are modeled here as
 * task names + a simple access-permission check on the "recipient".
 *
 * Compile & run (CloudSim 3.0.3 jars: cloudsim-3.0.3.jar):
 *   javac -cp cloudsim-3.0.3.jar SecureFileSharingSimulation.java
 *   java  -cp .:cloudsim-3.0.3.jar SecureFileSharingSimulation
 */
public class SecureFileSharingSimulation {

    public static void main(String[] args) {
        // Log a friendly header
        Log.printLine("========== Secure File Sharing Simulation (CloudSim) ==========");

        // 1. Initialise the CloudSim simulation engine
        int numUser = 1;
        Calendar calendar = Calendar.getInstance();
        boolean traceFlag = false;
        CloudSim.init(numUser, calendar, traceFlag);

        // 2. Create two datacenters (primary + backup for redundancy)
        Datacenter datacenter0 = createDatacenter("Datacenter_Primary");
        Datacenter datacenter1 = createDatacenter("Datacenter_Backup");

        // 3. Create the broker (represents our cloud account / tenant)
        DatacenterBroker broker = createBroker();
        int brokerId = broker.getId();

        // 4. Create one VM for the file-sharing service
        Vm vm = createVm(brokerId, 1);
        List<Vm> vmList = new ArrayList<>();
        vmList.add(vm);
        broker.submitVmList(vmList);

        // 5. Create the secure-file-sharing workload (cloudlets)
        List<Cloudlet> cloudletList = new ArrayList<>();
        cloudletList.add(makeCloudlet(brokerId, vm.getId(), 0, 40000, "FileEncrypt (AES-256)"));
        cloudletList.add(makeCloudlet(brokerId, vm.getId(), 1, 20000, "FileUpload (to cloud storage)"));
        cloudletList.add(makeCloudlet(brokerId, vm.getId(), 2, 20000, "FileDownload (by recipient)"));
        cloudletList.add(makeCloudlet(brokerId, vm.getId(), 3, 40000, "FileDecrypt (AES-256)"));
        cloudletList.add(makeCloudlet(brokerId, vm.getId(), 4,  8000, "AccessAuditRecord"));
        broker.submitCloudletList(cloudletList);

        // 6. Simulate an access-control decision before the file is shared
        boolean recipientAllowed = checkAccess("alice@cdct.org", "secure-app-users");
        Log.printLine("Access-control check: recipient allowed = " + recipientAllowed);

        // 7. Run the simulation
        CloudSim.startSimulation();
        CloudSim.stopSimulation();

        // 8. Report results
        List<Cloudlet> finished = broker.getCloudletReceivedList();
        printCloudletList(finished);

        Log.printLine("SecureFileSharingSimulation finished!");
    }

    /** A cloudlet is one step of the secure file-sharing workflow. */
    private static Cloudlet makeCloudlet(int brokerId, int vmId, int id,
                                         int length, String name) {
        UtilizationModel util = new UtilizationModelFull();
        Cloudlet c = new Cloudlet(id, length, 1, 300, 300, util, util, util);
        c.setUserId(brokerId);
        c.setVmId(vmId);
        c.setCloudletName(name);
        return c;
    }

    /** Simplified "authorization service": is the recipient a member of the allowed group? */
    private static boolean checkAccess(String user, String requiredGroup) {
        // In a real system this queries an identity provider / policy engine.
        return "alice@cdct.org".equals(user) && "secure-app-users".equals(requiredGroup);
    }

    private static Vm createVm(int brokerId, int id) {
        return new Vm(id, brokerId, 1000 /* mips */, 1 /* pesNumber */,
                      512 /* ram MB */, 1000 /* bw Mbps */, 10000 /* size MB */,
                      "Xen", new CloudletSchedulerTimeShared());
    }

    private static DatacenterBroker createBroker() {
        try {
            return new DatacenterBroker("Broker_CDCT");
        } catch (Exception e) {
            throw new RuntimeException("Could not create broker: " + e.getMessage(), e);
        }
    }

    private static Datacenter createDatacenter(String name) {
        List<Host> hostList = new ArrayList<>();
        List<Pe> peList = new ArrayList<>();
        peList.add(new Pe(0, new PeProvisionerSimple(2000)));  // 1 x 2000 MIPS core
        Host host = new Host(0, new RamProvisionerSimple(2048),
                new BwProvisionerSimple(10000), 1000000, peList,
                new VmSchedulerTimeShared(peList));
        hostList.add(host);

        String arch = "x86";
        String os = "Linux";
        String vmm = "Xen";
        double timeZone = 10.0;
        double costPerSec = 3.0;
        double costPerMem = 0.05;
        double costPerStorage = 0.1;
        double costPerBw = 0.1;

        DatacenterCharacteristics characteristics = new DatacenterCharacteristics(
                arch, os, vmm, hostList, timeZone, costPerSec, costPerMem,
                costPerStorage, costPerBw);

        try {
            return new Datacenter(name, characteristics, new VmAllocationPolicySimple(hostList),
                    new LinkedList<Storage>(), 0);
        } catch (Exception e) {
            throw new RuntimeException("Could not create datacenter: " + e.getMessage(), e);
        }
    }

    /** Print the finished cloudlets in the classic CloudSim table format. */
    private static void printCloudletList(List<Cloudlet> list) {
        Log.printLine();
        Log.printLine("========== OUTPUT ==========");
        String indent = "    ";
        Log.printLine(indent + "Cloudlet_ID" + indent + "Status" + indent
                + "Datacenter_ID" + indent + "VM_ID" + indent + "Time" + indent
                + "Start_Time" + indent + "Finish_Time" + indent + "Cost");
        DecimalFormat dft = new DecimalFormat("###.##");
        double totalCost = 0;
        for (Cloudlet cloudlet : list) {
            int status = cloudlet.getCloudletStatus();
            double time = cloudlet.getActualCPUTime();
            double start = cloudlet.getExecStartTime();
            double finish = cloudlet.getFinishTime();
            double cost = cloudlet.getProcessingCost();
            totalCost += cost;
            Log.printLine(indent + cloudlet.getCloudletId() + indent
                    + cloudletStatus(status) + indent
                    + cloudlet.getResourceId() + indent
                    + cloudlet.getVmId() + indent
                    + dft.format(time) + indent
                    + dft.format(start) + indent
                    + dft.format(finish) + indent
                    + dft.format(cost));
        }
        Log.printLine("Total execution cost of the secure file-sharing workflow: $"
                + dft.format(totalCost));
    }

    private static String cloudletStatus(int status) {
        switch (status) {
            case Cloudlet.SUCCESS: return "SUCCESS";
            case Cloudlet.FAILED:  return "FAILED";
            case Cloudlet.CANCELED: return "CANCELED";
            default: return "?";
        }
    }
}
