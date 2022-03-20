(ns enum)

; flatten by one level
(defn flat [ls]
  (apply conj [] ls))

(defn pairs [[head & tail]]
  (if (empty? tail)
    []
    (apply conj (map #(vector head %) tail) (pairs tail))))

(defn combinations [N ls]
  (if (or (< N 2) (empty? ls))
    (mapv vector ls)
    (concat
      (mapv (partial concat [(first ls)]) (combinations (- N 1) (rest ls)))
      (combinations N (rest ls))
      )
    ))

(defn has [v ls] (< 0 (count (filter (partial = v) ls))))
(defn enumerate [ls] (zipmap (range (count ls)) ls))
(defn zip [a b] (map-indexed (fn [i A] [A (nth b i)]) a))
(defn slice
  ([ls start] (drop start ls))
  ([ls start end] (take (- end start) (slice ls start)))
  ([ls start end step]
   (if (> step 0)
     (take-nth step (slice ls start end))
     (slice (reverse ls) (- (count ls) end) (- (count ls) start) (- 0 step))
     ))
  )

