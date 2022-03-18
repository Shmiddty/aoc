(ns cartesian)

(use '[enum :only (enumerate, zip)])

(defn flatgrid [lines] (apply conj [] (mapcat
    (fn [[y row]] (map (fn [[x c]] [[x y] c]) (enumerate row)))
    (enumerate lines)
    )))

(defn grid [lines]
  (->> lines
       (flatgrid)
       ;(filter #(< 0 (second %)))
       (map (partial apply hash-map))
       (apply merge)
       ))

(defn addvec [a b] (map (partial reduce +) (zip a b)))

(def dirs [
   [-1 -1] [0 -1] [1 -1]
   [-1  0]        [1  0]
   [-1  1] [0  1] [1  1]
   ])

(def neighbors (memoize (fn [pt] (map (partial addvec pt) dirs))))

(def fastneighbors (memoize (fn [[x y]] [
   [(- x 1) (- y 1)] [(+ x 0) (- y 1)] [(+ x 1) (- y 1)]
   [(- x 1) (+ y 0)]                   [(+ x 1) (+ y 0)]
   [(- x 1) (+ y 1)] [(+ x 0) (+ y 1)] [(+ x 1) (+ y 1)]
   ])))

