(ns io)

(defn read-all
  []
  (slurp *in*))

(defn read-lines
  []
  (line-seq (java.io.BufferedReader. *in*)))

(defn read-all-lines
  []
  (-> (read-all)
      (clojure.string/split #"\n")
      ))

(defn debug [v]
  (->> [v (println "DEBUG:" v)]
       (first)))

