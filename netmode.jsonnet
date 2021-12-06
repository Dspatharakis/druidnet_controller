local kp =
  (import 'kube-prometheus/main.libsonnet') +
  // Uncomment the following imports to enable its patches
  // (import 'kube-prometheus/addons/anti-affinity.libsonnet') +
  // (import 'kube-prometheus/addons/managed-cluster.libsonnet') +
 (import 'kube-prometheus/addons/node-ports.libsonnet') +
  // (import 'kube-prometheus/addons/static-etcd.libsonnet') +
 (import 'kube-prometheus/addons/custom-metrics.libsonnet') +
  // (import 'kube-prometheus/addons/external-metrics.libsonnet') +
  {
    values+:: {
      common+: {
        namespace: 'monitoring',
      },
    },

  exampleApplication: {
    prometheusRuleExample: {
      apiVersion: 'monitoring.coreos.com/v1',
      kind: 'PrometheusRule',
      metadata: {
        name: 'druidnet-rule',
        namespace: $.values.common.namespace,
      },
      spec: {
        groups: [
          {
            name: 'druidnet_rules',
            interval: '30s',
            rules: [
              {
                record: 'edge_server_request_rate_for_30',
                expr: 'rate(flask_http_request_total{service="web"} [30s])',
              },
              {
                record: 'edge_server_art_for_30',
                expr: 'rate(flask_http_request_duration_seconds_sum{service="web"} [30s]) / rate(flask_http_request_duration_seconds_count{service="web"} [30s])
                ',
              },
              {
                record: 'edge_server_cpu_for_60',
                expr: 'rate(container_cpu_usage_seconds_total{pod=~"web.*", container="web"}[60s])',
              },
              {
                record: 'edge_server_memory',
                expr: 'container_memory_working_set_bytes{pod=~"web.*", container="web"}',
              },
              {
                record: 'edge_server_pod_count',
                expr: 'count(count by (pod)(flask_http_request_total{pod=~"web.*", container="web"}))',
              },
            ],
          },
        ],
      },
    },
  },
};


{ 'setup/0namespace-namespace': kp.kubePrometheus.namespace } +
{
  ['setup/prometheus-operator-' + name]: kp.prometheusOperator[name]
  for name in std.filter((function(name) name != 'serviceMonitor' && name != 'prometheusRule'), std.objectFields(kp.prometheusOperator))
} +
// serviceMonitor and prometheusRule are separated so that they can be created after the CRDs are ready
{ 'prometheus-operator-serviceMonitor': kp.prometheusOperator.serviceMonitor } +
{ 'prometheus-operator-prometheusRule': kp.prometheusOperator.prometheusRule } +
{ 'kube-prometheus-prometheusRule': kp.kubePrometheus.prometheusRule } +
{ ['alertmanager-' + name]: kp.alertmanager[name] for name in std.objectFields(kp.alertmanager) } +
{ ['blackbox-exporter-' + name]: kp.blackboxExporter[name] for name in std.objectFields(kp.blackboxExporter) } +
{ ['grafana-' + name]: kp.grafana[name] for name in std.objectFields(kp.grafana) } +
{ ['kube-state-metrics-' + name]: kp.kubeStateMetrics[name] for name in std.objectFields(kp.kubeStateMetrics) } +
{ ['kubernetes-' + name]: kp.kubernetesControlPlane[name] for name in std.objectFields(kp.kubernetesControlPlane) }
{ ['node-exporter-' + name]: kp.nodeExporter[name] for name in std.objectFields(kp.nodeExporter) } +
{ ['prometheus-' + name]: kp.prometheus[name] for name in std.objectFields(kp.prometheus) } +
{ ['prometheus-adapter-' + name]: kp.prometheusAdapter[name] for name in std.objectFields(kp.prometheusAdapter) }
