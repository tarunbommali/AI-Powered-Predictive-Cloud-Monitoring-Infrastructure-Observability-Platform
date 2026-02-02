// import React, { useEffect, useState } from "react";
// import { Server } from "lucide-react";

// const InstancesPage = () => {
//   const [instances, setInstances] = useState([]);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     fetch("http://localhost:8000/api/instances", {
//       headers: {
//         Authorization: `Bearer ${localStorage.getItem("token")}`,
//       },
//     })
//       .then((res) => res.json())
//       .then((data) => {
//         setInstances(data);
//         setLoading(false);
//       })
//       .catch((err) => {
//         console.error("Error fetching instances:", err);
//         setLoading(false);
//       });
//   }, []);

//   return (
//     <div className="space-y-6 animate-in">
//       {/* Header */}
//       <div>
//         <h1 className="text-3xl font-bold gradient-text">Instances</h1>
//         <p className="text-gray-600 dark:text-gray-400 mt-1">
//           Manage your EC2 instances
//         </p>
//       </div>

//       {/* Loading */}
//       {loading && (
//         <div className="glass-card p-10 text-center">
//           <p className="text-gray-500">Loading instances...</p>
//         </div>
//       )}

//       {/* Empty State */}
//       {!loading && instances.length === 0 && (
//         <div className="glass-card p-12 text-center">
//           <Server className="w-16 h-16 text-primary-500 mx-auto mb-4" />
//           <h3 className="text-xl font-semibold mb-2">No Instances Found</h3>
//           <p className="text-gray-600 dark:text-gray-400">
//             Add an instance to start monitoring
//           </p>
//         </div>
//       )}

//       {/* Instances Table */}
//       {!loading && instances.length > 0 && (
//         <div className="glass-card overflow-x-auto">
//           <table className="w-full">
//             <thead>
//               <tr className="border-b border-gray-200 dark:border-gray-700">
//                 <th className="p-4 text-left">Name</th>
//                 <th className="p-4 text-left">Instance ID</th>
//                 <th className="p-4 text-left">IP Address</th>
//                 <th className="p-4 text-left">Status</th>
//                 <th className="p-4 text-left">Region</th>
//               </tr>
//             </thead>
//             <tbody>
//               {instances.map((instance) => (
//                 <tr
//                   key={instance.id}
//                   className="border-b border-gray-100 dark:border-gray-800"
//                 >
//                   <td className="p-4 font-medium">{instance.name}</td>
//                   <td className="p-4">{instance.instance_id}</td>
//                   <td className="p-4">{instance.ip_address}</td>
//                   <td className="p-4">
//                     <span
//                       className={`px-3 py-1 rounded-full text-sm ${
//                         instance.status === "running"
//                           ? "bg-green-100 text-green-700"
//                           : "bg-gray-100 text-gray-600"
//                       }`}
//                     >
//                       {instance.status}
//                     </span>
//                   </td>
//                   <td className="p-4">{instance.region || "-"}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}
//     </div>
//   );
// };

// export default InstancesPage;
import React, { useEffect, useState } from "react";
import { Server } from "lucide-react";
import { instancesAPI } from "../services/api"; // adjust path if needed

const InstancesPage = () => {
  const [instances, setInstances] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    instancesAPI
      .list()
      .then((res) => {
        setInstances(res.data);
      })
      .catch((err) => {
        console.error("Error fetching instances:", err);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6 animate-in">
      <div>
        <h1 className="text-3xl font-bold gradient-text">Instances</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Manage your EC2 instances
        </p>
      </div>

      {loading && (
        <div className="glass-card p-10 text-center">
          <p className="text-gray-500">Loading instances...</p>
        </div>
      )}

      {!loading && instances.length === 0 && (
        <div className="glass-card p-12 text-center">
          <Server className="w-16 h-16 text-primary-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">No Instances Found</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Add an instance to start monitoring
          </p>
        </div>
      )}

      {!loading && instances.length > 0 && (
        <div className="glass-card overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="p-4 text-left">Name</th>
                <th className="p-4 text-left">Instance ID</th>
                <th className="p-4 text-left">IP</th>
                <th className="p-4 text-left">Status</th>
                <th className="p-4 text-left">Region</th>
              </tr>
            </thead>
            <tbody>
              {instances.map((i) => (
                <tr key={i.id}>
                  <td className="p-4">{i.name}</td>
                  <td className="p-4">{i.instance_id}</td>
                  <td className="p-4">{i.ip_address}</td>
                  <td className="p-4">{i.status}</td>
                  <td className="p-4">{i.region || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default InstancesPage;
